import sys, os, shutil, re
from PyQt5.QtWidgets import QApplication, QFrame, QCheckBox, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from GPIOConf import GPIOConf

def Extract_APB3GPIO(template_file="demo/RISCV/APB3GPIO.v"):
    """读取文件并提取Apb3GPIORouter模块的内容，返回文件内容和Apb3GPIORouter内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3GPIORouter 模块
    match = re.search(r"(module\s+Apb3GPIORouter\b.*?endmodule)", content, re.S)
    if match:
        apb3gpiouter_content = match.group(1)
        return content, apb3gpiouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3GPIORouter 模块！")

def GPIO_Gen(modules, template_file="demo/RISCV/APB3GPIO.v", output_file="Apb3GPIO.v"):
    # 获取整个模板文件内容和 Apb3GPIORouter 模块内容
    full_content, apb3gpiouter_template = Extract_APB3GPIO(template_file)

    # 模板代码片段
    gpio_port_template = "    input wire [15:0] AFIO{name},\n    inout wire [15:0] GPIO{name},"
    signal_template = """
    // GPIO{name}
    wire [ 2:0] io_apb_PADDR_{name} = io_apb_PADDR[4:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    Apb3GPIO Apb3GPIO{name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .AFIO          (AFIO{name}),
        .GPIO          (GPIO{name})
    );
    """

    # 初始化模块的各个部分内容
    gpio_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (name, _) in enumerate(modules.items()):
        gpio_ports += gpio_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3GPIORouter 模块内容
    apb3gpiouter_code = apb3gpiouter_template.format(
        gpio_ports=gpio_ports.strip()[:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3GPIORouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3gpiouter_template, apb3gpiouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def Extract_APB3USART(template_file="demo/RISCV/APB3USART.v"):
    """读取文件并提取 Apb3USARTRouter 模块的内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3USARTRouter 模块
    match = re.search(r"(module\s+Apb3USARTRouter\b.*?endmodule)", content, re.S)
    if match:
        apb3usarrouter_content = match.group(1)
        return content, apb3usarrouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3USARTRouter 模块！")

def UART_Gen(modules, template_file="demo/RISCV/APB3USART.v", output_file="Apb3USART.v"):
    # 获取整个模板文件内容和 Apb3USARTRouter 模块内容
    full_content, apb3usarrouter_template = Extract_APB3USART(template_file)

    # 模板代码片段
    usart_port_template = "    input  wire {name}_RX,\n    output wire {name}_TX,\n    output wire {name}_interrupt,"
    signal_template = """
    // {name}
    wire [ 2:0] io_apb_PADDR_{name} = io_apb_PADDR[4:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    Apb3USART Apb3{name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .USART_RX      ({name}_RX),
        .USART_TX      ({name}_TX),
        .interrupt     ({name}_interrupt)
    );
    """

    # 初始化模块的各个部分内容
    usart_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (key, _) in enumerate(modules.items()):
        name = f"USART{key}"
        usart_ports += usart_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3USARTRouter 模块内容
    apb3usarrouter_code = apb3usarrouter_template.format(
        usart_ports=usart_ports.strip()[:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3USARTRouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3usarrouter_template, apb3usarrouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def Extract_APB3I2C(template_file="demo/RISCV/APB3I2C.v"):
    """读取文件并提取Apb3I2CRouter模块的内容，返回文件内容和Apb3I2CRouter内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3I2CRouter 模块
    match = re.search(r"(module\s+Apb3I2CRouter\b.*?endmodule)", content, re.S)
    if match:
        apb3i2crouter_content = match.group(1)
        return content, apb3i2crouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3I2CRouter 模块！")

def I2C_Gen(modules, template_file="demo/RISCV/APB3I2C.v", output_file="Apb3I2C.v"):
    # 获取整个模板文件内容和 Apb3I2CRouter 模块内容
    full_content, apb3i2crouter_template = Extract_APB3I2C(template_file)

    # 模板代码片段
    i2c_port_template = "    input  wire {name}_SDA,\n    output wire {name}_SCL,\n    output wire {name}_interrupt,"
    signal_template = """
    // {name}
    wire [ 3:0] io_apb_PADDR_{name} = io_apb_PADDR[5:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    Apb3I2C Apb3{name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .I2C_SDA       ({name}_SDA),
        .I2C_SCL       ({name}_SCL),
        .interrupt     ({name}_interrupt)
    );
    """

    # 初始化模块的各个部分内容
    i2c_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (key, _) in enumerate(modules.items()):
        name = f"I2C{key}"
        i2c_ports += i2c_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3I2CRouter 模块内容
    apb3i2crouter_code = apb3i2crouter_template.format(
        i2c_ports=i2c_ports.strip()[:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3I2CRouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3i2crouter_template, apb3i2crouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def Extract_APB3SPI(template_file="demo/RISCV/APB3SPI.v"):
    """读取文件并提取Apb3SPIRouter模块的内容，返回文件内容和Apb3SPIRouter内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3SPIRouter 模块
    match = re.search(r"(module\s+Apb3SPIRouter\b.*?endmodule)", content, re.S)
    if match:
        apb3spirouter_content = match.group(1)
        return content, apb3spirouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3SPIRouter 模块！")

def SPI_Gen(modules, template_file="demo/RISCV/APB3SPI.v", output_file="Apb3SPI.v"):
    # 获取整个模板文件内容和 Apb3SPIRouter 模块内容
    full_content, apb3spirouter_template = Extract_APB3SPI(template_file)

    # 模板代码片段
    spi_port_template = """    output wire {name}_SCK,\n    output wire {name}_MOSI,\n    input  wire {name}_MISO,\n    output wire {name}_CS,\n    output wire {name}_interrupt,"""
    signal_template = """
    // {name}
    wire [ 3:0] io_apb_PADDR_{name} = io_apb_PADDR[5:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    Apb3SPI Apb3SPI{name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .SPI_SCK       ({name}_SCK),
        .SPI_MOSI      ({name}_MOSI),
        .SPI_MISO      ({name}_MISO),
        .SPI_CS        ({name}_CS),
        .interrupt     ({name}_interrupt)
    );
    """

    # 初始化模块的各个部分内容
    spi_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (key, _) in enumerate(modules.items()):
        name = f"SPI{key}"
        spi_ports += spi_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3SPIRouter 模块内容
    apb3spirouter_code = apb3spirouter_template.format(
        spi_ports=spi_ports.strip()[0:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3SPIRouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3spirouter_template, apb3spirouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def Extract_APB3TIM(template_file="demo/RISCV/APB3TIM.v"):
    """读取文件并提取Apb3TIMRouter模块的内容，返回文件内容和Apb3TIMRouter内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3TIMRouter 模块
    match = re.search(r"(module\s+Apb3TIMRouter\b.*?endmodule)", content, re.S)
    if match:
        apb3timrouter_content = match.group(1)
        return content, apb3timrouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3TIMRouter 模块！")

def TIM_Gen(modules, template_file="demo/RISCV/APB3TIM.v", output_file="Apb3TIM.v"):
    # 获取整个模板文件内容和 Apb3TIMRouter 模块内容
    full_content, apb3timrouter_template = Extract_APB3TIM(template_file)

    # 模板代码片段
    tim_port_template = "    output wire [3:0] {name}_CH,\n    output wire       {name}_interrupt,"
    signal_template = """
    // {name}
    wire [ 4:0] io_apb_PADDR_{name} = io_apb_PADDR[6:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    Apb3TIM Apb3TIM{name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .TIM_CH        ({name}_CH),
        .interrupt     ({name}_interrupt)
    );
    """

    # 初始化模块的各个部分内容
    tim_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (key, _) in enumerate(modules.items()):
        name = f"TIM{key}"
        tim_ports += tim_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3TIMRouter 模块内容
    apb3timrouter_code = apb3timrouter_template.format(
        tim_ports=tim_ports.strip()[:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3TIMRouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3timrouter_template, apb3timrouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def Extract_APB3WDG(template_file="demo/RISCV/APB3WDG.v"):
    """读取文件并提取Apb3WDGRouter模块的内容，返回文件内容和Apb3WDGRouter模块内容"""
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 提取 Apb3WDGRouter 模块
    match = re.search(r"(module\s+Apb3WDGRouter\b.*?endmodule)", content, re.S)
    if match:
        apb3wdgrouter_content = match.group(1)
        return content, apb3wdgrouter_content
    else:
        raise ValueError("模板文件中未找到 Apb3WDGRouter 模块！")

def WDG_Gen(modules, template_file="demo/RISCV/APB3WDG.v", output_file="Apb3WDG.v"):
    # 获取整个模板文件内容和 Apb3WDGRouter 模块内容
    full_content, apb3wdgrouter_template = Extract_APB3WDG(template_file)

    # 模板代码片段
    wdg_port_template = "    output wire {name},"
    signal_template = """
    // {name}
    wire [ 1:0] io_apb_PADDR_{name} = io_apb_PADDR[3:2];
    wire        io_apb_PSEL_{name} = Apb3PSEL[{index}];
    wire        io_apb_PENABLE_{name} = io_apb_PENABLE;
    wire        io_apb_PREADY_{name};
    wire        io_apb_PWRITE_{name} = io_apb_PWRITE;
    wire [31:0] io_apb_PWDATA_{name} = io_apb_PWDATA;
    wire [31:0] io_apb_PRDATA_{name};
    wire        io_apb_PSLVERROR_{name} = 1'b0;
    """
    case_template = """                16'h{case_hex}: begin
                    _zz_io_apb_PREADY = io_apb_PREADY_{name};
                    _zz_io_apb_PRDATA = io_apb_PRDATA_{name};
                    _zz_io_apb_PSLVERROR = io_apb_PSLVERROR_{name};
                end"""
    psel_assignment_template = """            Apb3PSEL[{index}] = ((io_apb_PADDR[15:12] == 4'd{addr}) && io_apb_PSEL[0]);  // {name}"""
    module_instance_template = """
    {name} {name} (
        .io_apb_PCLK   (io_apb_PCLK),
        .io_apb_PRESET (io_apb_PRESET),
        .io_apb_PADDR  (io_apb_PADDR_{name}),
        .io_apb_PSEL   (io_apb_PSEL_{name}),
        .io_apb_PENABLE(io_apb_PENABLE_{name}),
        .io_apb_PREADY (io_apb_PREADY_{name}),
        .io_apb_PWRITE (io_apb_PWRITE_{name}),
        .io_apb_PWDATA (io_apb_PWDATA_{name}),
        .io_apb_PRDATA (io_apb_PRDATA_{name}),
        .{name}_rst      ({name}_rst)
    );
    """

    # 初始化模块的各个部分内容
    wdg_ports = ""
    module_signals = ""
    case_statements = ""
    psel_assignments = ""
    module_instances = ""
    # 为每个模块生成对应的 Verilog 代码片段
    for index, (name, _) in enumerate(modules.items()):
        wdg_ports += wdg_port_template.format(name=name) + "\n"
        module_signals += signal_template.format(name=name, index=index)
        case_statements += case_template.format(case_hex=f"{1 << index:04x}", name=name) + "\n"
        psel_assignments += psel_assignment_template.format(index=index, addr=index, name=name) + "\n"
        module_instances += module_instance_template.format(name=name)
    # 格式化 Apb3WDGRouter 模块内容
    apb3wdgrouter_code = apb3wdgrouter_template.format(
        wdg_ports=wdg_ports.strip()[:-1],
        module_signals=module_signals.strip(),
        case_statements=case_statements.strip(),
        psel_assignments=psel_assignments.strip(),
        module_instances=module_instances.strip()
    )
    # 将格式化后的 Apb3WDGRouter 模块替换回原始文件内容中
    updated_content = full_content.replace(apb3wdgrouter_template, apb3wdgrouter_code)
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(updated_content)
    # print(f"'{output_file}' 生成成功。")
    return updated_content

def RCC_Gen(output_file="AhbRCC.v"):
    content = ""
    with open("demo/RISCV/AHBRCC.v", "r", encoding="utf-8") as f:
        content += f.read()
    # with open(output_file, "w") as f:
    #     f.write(content)
    # print(f"'{output_file}' 生成成功。")
    return content

def DMA_Gen(output_file="AhbDMA.v"):
    content = ""
    with open("demo/RISCV/AHBDMA.v", "r", encoding="utf-8") as f:
        content += f.read()
    # with open(output_file, "w") as f:
    #     f.write(content)
    # print(f"'{output_file}' 生成成功。")
    return content

def DVP_Gen(output_file="AHBDVP.v"):
    content = ""
    file_paths = [
        "demo/RISCV/AHBDVP.v",
        "demo/RISCV/AHBVI.v",
        "demo/RISCV/AHBVP.v",
        "demo/RISCV/AHBVO.v",
        "demo/VP/binarizer.v",
        "demo/VP/cutter.v",
        "demo/VP/edger.v",
        "demo/VP/filler.v",
        "demo/VP/filter.v",
        "demo/VP/rgb2ycbcr.v",
        "demo/VP/scaler.v"
    ]
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            content += f.read() + "\n\n"
    # 写入新文件
    # with open(output_file, "w") as f:
    #     f.write(content)
    # print(f"'{output_file}' 生成成功。")
    return content

def Top_Gen(DEVICES, output_file="Cyber.v"):
    """生成顶层文件 Top.v"""
    Cyber = ""

    Connection = ""
    for GPIO_port, AFIO in DEVICES["GPIO"].items():
        AFIO_connection = ""
        for i, pin in enumerate(AFIO):
            if pin:
                _, type = pin.split("_", 1)
                if type in ["RX", "MISO"]:
                    AFIO_connection += "1'bz, "
                    Connection += f"wire {pin} = AFIO{GPIO_port}[{16-i}];\n"
                else:
                    AFIO_connection += f"{pin}, "
                    Connection += f"wire {pin};\n"
            else:
                AFIO_connection += "1'bz, "
        AFIO_connection = AFIO_connection[:-2]
        Connection += f"wire [15:0] AFIO{GPIO_port} = " + "{" + AFIO_connection + "};\n"

    with open("demo/Cyber.v", "r", encoding="utf-8") as f:
        Cyber += f.read() + "\n\n"
    with open("demo/RISCV/VexRiscv.v", "r", encoding="utf-8") as f:
        Cyber += f.read() + "\n\n"
    with open("demo/RISCV/APB3RAM.v", "r", encoding="utf-8") as f:
        Cyber += f.read() + "\n\n"
    return Cyber

class NewPro(QDialog):
    def __init__(self):
        super().__init__()
        self.GPIOConf = GPIOConf()
        self.DEVICES = self.GPIOConf.DEVICES
        self.project_path = ""

        self.setWindowTitle("New Project")
        self.setWindowIcon(QIcon('icons/app.svg'))
        self.resize(400, 250)  # 增加窗口宽度
        self.setStyleSheet("background-color: #D1A7A4;")  # 将这里的颜色设置为你想要的颜色
        self.initUI()

    def initUI(self):
        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建项目名称输入标签和输入框
        project_name_layout = QHBoxLayout()
        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        self.project_name_input.setText("demo")
        project_name_layout.addWidget(self.project_name_label)
        project_name_layout.addWidget(self.project_name_input)
        main_layout.addLayout(project_name_layout)

        # 是否使用默认位置
        self.default_location_checkbox = QCheckBox("Use default location")
        self.default_location_checkbox.setChecked(True)
        self.default_location_checkbox.toggled.connect(self.toggle_location_input)
        self.browse_button = QPushButton("Browse")
        self.browse_button.setEnabled(False)
        self.browse_button.clicked.connect(self.browse_folder)
        location_layout = QHBoxLayout()
        location_layout.addWidget(self.default_location_checkbox)
        location_layout.addWidget(self.browse_button)
        main_layout.addLayout(location_layout)
        # 创建项目生成路径输入标签、输入框和按钮
        self.project_path_label = QLabel("Location:")
        self.project_path_input = QLineEdit()
        self.project_path_input.setText("../Workspace")
        self.project_path_input.setEnabled(False)
        location_layout = QHBoxLayout()
        location_layout.addWidget(self.project_path_label)
        location_layout.addWidget(self.project_path_input)
        main_layout.addLayout(location_layout)

        # 横条：分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # 硬件部分
        self.hardware_label = QLabel("Hardware")
        self.cyber_checkbox = QCheckBox("Cyber")
        self.cyber_checkbox.setChecked(True)
        hardware_layout = QHBoxLayout()
        hardware_layout.addWidget(self.hardware_label)
        hardware_layout.addStretch()  # 添加弹性空格
        hardware_layout.addWidget(self.cyber_checkbox)
        main_layout.addLayout(hardware_layout)
        # AHB 配置
        self.ahb_label = QLabel("AHB Device")
        self.ahb_checkbox = QCheckBox("Enable")
        self.ahb_checkbox.setChecked(True)
        self.ahb_checkbox.toggled.connect(self.toggle_ahb_config)
        self.ahb_button = QPushButton("DVP Conf")
        # self.ahb_button.clicked.connect(self.open_gpio_config)
        ahb_layout = QHBoxLayout()
        ahb_layout.addWidget(self.ahb_label)
        ahb_layout.addWidget(self.ahb_checkbox)
        ahb_layout.addWidget(self.ahb_button)
        main_layout.addLayout(ahb_layout)
        # APB 配置
        self.apb_label = QLabel("APB Device")
        self.apb_checkbox = QCheckBox("Enable")
        self.apb_checkbox.setChecked(True)
        self.apb_checkbox.toggled.connect(self.toggle_apb_config)
        self.apb_button = QPushButton("GPIO Conf")
        self.apb_button.clicked.connect(self.open_gpio_config)
        apb_layout = QHBoxLayout()
        apb_layout.addWidget(self.apb_label)
        apb_layout.addWidget(self.apb_checkbox)
        apb_layout.addWidget(self.apb_button)
        main_layout.addLayout(apb_layout)

        # 横条：分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # 软件部分
        self.software_label = QLabel("Software")
        main_layout.addWidget(self.software_label)
        # 工程模板，子模板标签
        template_label = QLabel("Template:")
        sub_template_label = QLabel("Sub-Temp:")
        template_layout = QHBoxLayout()
        template_layout.addWidget(template_label)
        template_layout.addWidget(sub_template_label)
        main_layout.addLayout(template_layout)
        # 工程模板和子模板下拉框
        self.template_combo = QComboBox()
        self.template_combo.addItems(["bare", "freertos", "rt-thread"])
        self.template_combo.currentIndexChanged.connect(self.update_options)
        self.sub_template_combo = QComboBox()
        self.update_options()
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.template_combo)
        combo_layout.addWidget(self.sub_template_combo)
        main_layout.addLayout(combo_layout)

        # 确认按钮
        self.confirm_button = QPushButton("Generate")
        self.confirm_button.clicked.connect(self.Generate)
        main_layout.addWidget(self.confirm_button)

        # 设置布局
        self.setLayout(main_layout)

    def browse_folder(self):
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # 如果选择了文件夹，则将路径显示到输入框
        if folder:
            self.project_path_input.setText(folder)

    def toggle_location_input(self):
        # 控制位置输入框和浏览按钮的使能状态
        is_default = self.default_location_checkbox.isChecked()
        self.project_path_input.setEnabled(not is_default)
        self.browse_button.setEnabled(not is_default)

    def toggle_ahb_config(self):
        # 控制 AHB 配置按钮的使能状态
        self.ahb_button.setEnabled(self.ahb_checkbox.isChecked())

    def toggle_apb_config(self):
        # 控制 APB 配置按钮的使能状态
        self.apb_button.setEnabled(self.apb_checkbox.isChecked())

    def open_gpio_config(self):
        # 创建并显示 GPIO 配置对话框
        if self.GPIOConf.exec_() == QDialog.Accepted:  # QDialog.Accepted 若用户点击了确定按钮
            self.DEVICES = self.GPIOConf.DEVICES

    def update_options(self):
        # 获取第一个选择框的选中项
        selected_template = self.template_combo.currentText()
        # 清空当前的动态选择框内容
        self.sub_template_combo.clear()
        # 根据第一个选择框的选项生成第二个选择框的内容
        if selected_template == "bare":
            self.sub_template_combo.addItems(["demo", "boot", "dvp", "led_breathe", "led_flow", "ov5640"])
        elif selected_template == "freertos":
            self.sub_template_combo.addItems(["demo1-blinky", "test"])
        elif selected_template == "rt-thread":
            self.sub_template_combo.addItems([
                "demo1-thread", "demo2-container", "demo3-delay", "demo4-muti_priority",
                "demo5-timer", "demo6-timeslice", "demo7-finsh", "demo7-finsh+", "test"
            ])

    def Generate(self):
        # 验证输入内容
        if not self.project_name_input.text():
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return
        if not self.project_path_input.text():
            QMessageBox.warning(self, "Warning", "Please input project location!")
            return

        # 获取项目名称和路径
        self.project_path = self.project_path_input.text() + '/' + self.project_name_input.text()
        # 复制模板工程到指定路径
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)  # 如果目标目录不存在，则创建它
        else:
            # 如果目标目录存在，则提示用户是否覆盖
            reply = QMessageBox.question(self, "Warning", "The project already exists, do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            # 如果用户选择覆盖，则先删除目标目录
            try:
                shutil.rmtree(self.project_path)
                os.makedirs(self.project_path, exist_ok=True)
            except Exception as e:
                print(e)
                return
        # 生成软件工程
        self.Generate_Software()
        # 生成硬件工程
        self.Generate_Hardware()
        # 关闭对话框
        self.accept()

    def Generate_BSP(self):
        if not self.DEVICES:
            return
        # 生成 cyber.h 配置文件
        cyber_start = ""
        DVP_STR = ""
        GPIO_STR = ""
        UART_STR = ""
        SPI_STR = ""
        I2C_STR = ""
        TIM_STR = ""
        WDG_STR = ""
        cyber_end = ""

        cyber_start += "#ifndef __CYBER_H_\n#define __CYBER_H_\n\n"
        cyber_start += "typedef enum{RESET = 0, SET = !RESET} FlagStatus, ITStatus;\n"
        cyber_start += "typedef enum{DISABLE = 0, ENABLE = !DISABLE} FunctionalState;\n"
        cyber_start += "typedef enum{ERROR = 0, SUCCESS = !ERROR} ErrorStatus;\n\n"
        cyber_start += '#include <stdint.h>\n#include "config.h"\n\n'
        cyber_start += "/*!< Base memory map */\n"
        cyber_start += "#define SRAM_BASE ((uint32_t)0x80000000)   /*!< SRAM base address */\n"
        cyber_start += "#define PERIPH_BASE ((uint32_t)0xF0000000) /*!< Peripheral base address */\n\n"
        cyber_start += "/*!< Peripheral memory map */\n"
        cyber_start += "#define APBPERIPH_BASE PERIPH_BASE\n"
        cyber_start += "#define AHBPERIPH_BASE (PERIPH_BASE + 0x1000000)\n\n"
        if self.ahb_checkbox.isChecked():
            DVP_STR += '#ifdef CYBER_DVP\n/*!< DVP */\n#include "dvp.h"\n'
            DVP_STR += "#define DVP_BASE (AHBPERIPH_BASE + 0x20000)\n"
            DVP_STR += "#define DVP ((DVP_TypeDef *)DVP_BASE) // 0xF1020000\n"
            DVP_STR += "#endif\n\n"
        if self.apb_checkbox.isChecked():
            if self.DEVICES["GPIO"] != {}:
                GPIO_BASE = "APBPERIPH_BASE + 0x00000"
                GPIO_STR += "#ifdef CYBER_GPIO\n/*!< GPIO */\n"
                GPIO_STR += '#include "gpio.h"\n'
                GPIO_STR += f"#define GPIO_BASE {GPIO_BASE}\n"
                for GPIO_port, _ in self.DEVICES["GPIO"].items():
                    index = ''.join(str(ord(char) - ord('A')) for char in GPIO_port if 'A' <= char <= 'Z')
                    GPIO_STR += f"#define GPIO{GPIO_port}_BASE (GPIO_BASE + 0x{index}000)\n"
                    GPIO_STR += f"#define GPIO{GPIO_port} ((GPIO_TypeDef *) GPIO{GPIO_port}_BASE)\n"
                GPIO_STR += "#endif\n\n"
            if self.DEVICES["UART"] != {}:
                UART_BASE = "APBPERIPH_BASE + 0x10000"
                UART_STR += "#ifdef CYBER_USART\n/*!< USART */\n"
                UART_STR += '#include "usart.h"\n'
                UART_STR += "#define UART_SAMPLE_PER_BAUD 5\n"
                UART_STR += f"#define USART_BASE {UART_BASE}\n"
                for UART_port, _ in self.DEVICES["UART"].items():
                    UART_STR += f"#define USART{UART_port}_BASE (USART_BASE + 0x{int(UART_port)-1}000)\n"
                    UART_STR += f"#define USART{UART_port} ((USART_TypeDef *) USART{UART_port}_BASE)\n"
                UART_STR += "#endif\n\n"
            if self.DEVICES["SPI"] != {}:
                SPI_BASE = "APBPERIPH_BASE + 0x20000"
                SPI_STR += "#ifdef CYBER_SPI\n/*!< SPI */\n"
                SPI_STR += '#include "spi.h"\n'
                SPI_STR += f"#define SPI_BASE {SPI_BASE}\n"
                for SPI_port, _ in self.DEVICES["SPI"].items():
                    SPI_STR += f"#define SPI{SPI_port}_BASE (SPI_BASE + 0x{int(SPI_port)-1}000)\n"
                    SPI_STR += f"#define SPI{SPI_port} ((SPI_TypeDef *) SPI{SPI_port}_BASE)\n"
                SPI_STR += "#endif\n\n"
            if self.DEVICES["I2C"] != {}:
                I2C_BASE = "APBPERIPH_BASE + 0x30000"
                I2C_STR += "#ifdef CYBER_I2C\n/*!< I2C */\n"
                I2C_STR += '#include "i2c.h"\n'
                I2C_STR += f"#define I2C_BASE {I2C_BASE}\n"
                for I2C_port, _ in self.DEVICES["I2C"].items():
                    I2C_STR += f"#define I2C{I2C_port}_BASE (I2C_BASE + 0x{int(I2C_port)-1}000)\n"
                    I2C_STR += f"#define I2C{I2C_port} ((I2C_TypeDef *) I2C{I2C_port}_BASE)\n"
                I2C_STR += "#endif\n\n"
            if self.DEVICES["TIM"] != {}:
                TIM_BASE = "APBPERIPH_BASE + 0x40000"
                TIM_STR += "#ifdef CYBER_TIM\n/*!< TIM */\n"
                TIM_STR += '#include "tim.h"\n'
                TIM_STR += f"#define TIM_BASE {TIM_BASE}\n"
                for TIM_port, _ in self.DEVICES["TIM"].items():
                    TIM_STR += f"#define TIM{TIM_port}_BASE (TIM_BASE + 0x{int(TIM_port)-1}000)\n"
                    TIM_STR += f"#define TIM{TIM_port} ((TIM_TypeDef *) TIM{TIM_port}_BASE)\n"
                TIM_STR += "#endif\n\n"
            for WDG_port, state in self.DEVICES["WDG"].items():
                if (WDG_port == "IWDG") & state:
                    WDG_STR += '#ifdef CYBER_IWDG\n/*!< IWDG */\n#include "iwdg.h"\n'
                    WDG_STR += f"#define {WDG_port}_BASE (0x50000 + 0x0000)\n"
                    WDG_STR += f"#define {WDG_port} ((IWDG_TypeDef *) {WDG_port}_BASE)\n"
                    WDG_STR += "#endif\n\n"
                elif (WDG_port == "WWDG") & state:
                    WDG_STR += '#ifdef CYBER_WWDG\n/*!< WWDG */\n#include "wwdg.h"\n'
                    WDG_STR += f"#define {WDG_port}_BASE (0x50000 + 0x1000)\n"
                    WDG_STR += f"#define {WDG_port} ((WWDG_TypeDef *) {WDG_port}_BASE)\n"
                    WDG_STR += "#endif\n\n"
        cyber_end += "#define assert_param(expr) ((void)0)\n\n#endif /* __CYBER_H_ */\n"

        return f"{cyber_start}{DVP_STR}{GPIO_STR}{UART_STR}{SPI_STR}{I2C_STR}{TIM_STR}{WDG_STR}{cyber_end}"

    def Generate_config(self):
        if not self.DEVICES:
            return
        # 生成 config.h 配置文件
        config = ""
        config += "#ifndef __CONFIG_H_\n#define __CONFIG_H_\n\n#define CORE_HZ 50000000\n\n"
        if self.apb_checkbox.isChecked():
            if self.DEVICES["GPIO"] != {}:
                config += "#define CYBER_GPIO\n"
            if self.DEVICES["UART"] != {}:
                config += "#define CYBER_USART\n"
            if self.DEVICES["SPI"] != {}:
                config += "#define CYBER_SPI\n"
            if self.DEVICES["I2C"] != {}:
                config += "#define CYBER_I2C\n"
            if self.DEVICES["TIM"] != {}:
                config += "#define CYBER_TIM\n"
            for WDG_port, state in self.DEVICES["WDG"].items():
                if (WDG_port == "IWDG") & state:
                    config += "#define CYBER_IWDG\n"
                elif (WDG_port == "WWDG") & state:
                    config += "#define CYBER_WWDG\n"
        if self.ahb_checkbox.isChecked():
            config += "#define CYBER_DVP\n"
        config += "\n#endif /* __CONFIG_H_ */\n"

        return config

    def Generate_Software(self):
        # 获取模板路径、工程名称、工程路径
        template_path = "/mnt/hgfs/share/Riscv-SoC-Software/projects/"
        selected_template = template_path + self.template_combo.currentText() + '/' + self.sub_template_combo.currentText()
        # 遍历源目录中的文件和文件夹
        for item in os.listdir(selected_template):
            if item == "build":
                continue
            source_item = os.path.join(selected_template, item)
            target_item = os.path.join(self.project_path, item)
            try:
                # 如果是文件，则进行复制
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, target_item)
                    # print(f"已复制文件: {source_item} 到 {target_item}")
                # 如果是目录，则递归复制文件夹内容
                elif os.path.isdir(source_item):
                    shutil.copytree(source_item, target_item, dirs_exist_ok=True)
                    # print(f"已复制目录: {source_item} 到 {target_item}")
            except Exception as e:
                print(e)
        # 生成 cyber.h 配置文件
        cyber = self.Generate_BSP()
        with open(self.project_path + "/libs/cyber.h", 'w', encoding='utf-8') as file:
            file.write(cyber)
        # 生成 config.h 配置文件
        try:
            config = self.Generate_config()
            with open(self.project_path + "/src/config.h", 'w', encoding='utf-8') as file:
                file.write(config)
        except:
            pass
        try:
            config = self.Generate_config()
            with open(self.project_path + "/user/config.h", 'w', encoding='utf-8') as file:
                file.write(config)
        except:
            pass
        # 生成 Makefile
        # 读取 gcc.mk 和 subproject.mk 的内容
        try:
            gcc_mk_path = template_path + self.template_combo.currentText() + "/gcc.mk"
            with open(gcc_mk_path, 'r', encoding='utf-8') as file:
                gcc_mk_content = file.read()
            subproject_mk_path = template_path + self.template_combo.currentText() + "/subproject.mk"
            with open(subproject_mk_path, 'r', encoding='utf-8') as file:
                subproject_mk_content = file.read()
        except FileNotFoundError as e:
            print(e)
            return
        # 替换 Makefile 中的 include 指令, 替换 name
        try:
            with open(self.project_path + "/Makefile", 'r', encoding='utf-8') as file:
                makefile_content = file.read()
            makefile_content = makefile_content.replace("include ../gcc.mk", gcc_mk_content)
            makefile_content = makefile_content.replace("include ../subproject.mk", subproject_mk_content)
            lines = makefile_content.splitlines()
            # 遍历每一行，找到包含 "PROJ_NAME =" 的行并替换
            for i in range(len(lines)):
                if lines[i].startswith("PROJ_NAME ="):
                    lines[i] = f"PROJ_NAME = {self.project_name_input.text()}"
            # 将修改后的行重新拼接成一个字符串
            new_makefile = "\n".join(lines)
            with open(self.project_path + "/Makefile", 'w', encoding='utf-8') as file:
                file.write(new_makefile)
        except Exception as e:
            print(e)

    # 生成顶层连接
    def Top_Connection_Gen(self):
        Connection = ""
        for GPIO_port, AFIO in self.DEVICES["GPIO"].items():
            AFIO_connection = ""
            for i, pin in enumerate(AFIO):
                if pin:
                    _, type = pin.split("_", 1)
                    if type in ["RX", "MISO"]:
                        AFIO_connection += "1'bz, "
                        Connection += f"wire {pin} = AFIO{GPIO_port}[{16-i}];\n"
                    else:
                        AFIO_connection += f"{pin}, "
                        Connection += f"wire {pin};\n"
                else:
                    AFIO_connection += "1'bz, "
            AFIO_connection = AFIO_connection[:-2]
            Connection += f"wire [15:0] AFIO{GPIO_port} = " + "{" + AFIO_connection + "};\n"
        print(Connection)

    def Generate_Hardware(self):
        Cyber = ""
        APB = ""
        AHB = ""
        if self.apb_checkbox.isChecked():
            with open("demo/RISCV/APB3BUS.v", "r", encoding="utf-8") as f:
                APB += f.read()
            if self.DEVICES["GPIO"] != {}:
                APB += GPIO_Gen(self.DEVICES["GPIO"]) + "\n\n"
            if self.DEVICES["UART"] != {}:
                APB += UART_Gen(self.DEVICES["UART"]) + "\n\n"
            if self.DEVICES["I2C"] != {}:
                APB += I2C_Gen(self.DEVICES["I2C"]) + "\n\n"
            if self.DEVICES["SPI"] != {}:
                APB += SPI_Gen(self.DEVICES["SPI"]) + "\n\n"
            if self.DEVICES["TIM"] != {}:
                APB += TIM_Gen(self.DEVICES["TIM"]) + "\n\n"
            if self.DEVICES["WDG"] != {}:
                APB += WDG_Gen(self.DEVICES["WDG"]) + "\n\n"
        if self.ahb_checkbox.isChecked():
            with open("demo/RISCV/AHBBUS.v", "r", encoding="utf-8") as f:
                AHB += f.read() + "\n\n"
            AHB += RCC_Gen() + "\n\n"
            AHB += DMA_Gen() + "\n\n"
            AHB += DVP_Gen() + "\n\n"
        if self.cyber_checkbox.isChecked():
            Cyber += Top_Gen(self.DEVICES) + "\n\n"

        # 写入新文件
        # with open("./Cyber.v", "w") as f:
        #     f.write(Cyber + APB + AHB)
        with open(f"{self.project_path}/Cyber.v", "w") as f:
            f.write(Cyber + APB + AHB)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NewPro()
    dialog.exec_()

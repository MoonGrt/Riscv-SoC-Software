import re

def read_and_extract_apb3wdgrouter(template_file="demo\RISCV\APB3WDG.v"):
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

def generate_verilog_top(modules, template_file="demo\RISCV\APB3WDG.v", output_file="Apb3WDG.v"):
    # 获取整个模板文件内容和 Apb3WDGRouter 模块内容
    full_content, apb3wdgrouter_template = read_and_extract_apb3wdgrouter(template_file)

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
    with open(output_file, "w") as f:
        f.write(updated_content)
    print(f"Verilog 顶层文件 '{output_file}' 生成成功。")






if __name__ == "__main__":
    modules = {"IWDG": True, "WWDG": True}
    generate_verilog_top(modules)

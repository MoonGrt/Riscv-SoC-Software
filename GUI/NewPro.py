import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QFrame, QCheckBox, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from GPIOConf import GPIOConf

class NewPro(QDialog):
    def __init__(self):
        super().__init__()
        self.GPIOConf = GPIOConf()
        self.DEVICES = self.GPIOConf.DEVICES

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
        self.ahb_button = QPushButton("Configration")
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
        self.apb_button = QPushButton("Configration")
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
            # 生成 SoC 代码
            self.Generate_Hardware()
            # 生成 Libs
            self.Generate_Software()

    def update_options(self):
        # 获取第一个选择框的选中项
        selected_template = self.template_combo.currentText()
        # 清空当前的动态选择框内容
        self.sub_template_combo.clear()
        # 根据第一个选择框的选项生成第二个选择框的内容
        if selected_template == "bare":
            self.sub_template_combo.addItems(["demo", "boot", "dvp", "led_breathe", "led_flow"])
        elif selected_template == "freertos":
            self.sub_template_combo.addItems(["demo1-blinky", "test"])
        elif selected_template == "rt-thread":
            self.sub_template_combo.addItems([
                "demo1-thread", "demo2-container", "demo3-delay", "demo4-muti_priority",
                "demo5-timer", "demo6-timeslice", "demo7-finish", "demo7-finish+", "test"
            ])

    def Generate(self):
        # 生成软件工程
        self.Generate_Software()
        # 生成硬件工程
        # self.Generate_Hardware()
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
        template_path = "../projects/"
        selected_template = template_path + self.template_combo.currentText() + '/' + self.sub_template_combo.currentText()
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

    # 生成顶层连接
    def Top_Connection_Gen(self):
        Connection = ""
        for GPIO_port, AFIO in self.GPIOS.items():
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

    def GPIO_Gen(self):
        pass

    def SPI_Gen(self):
        pass

    def I2C_Gen(self):
        pass

    def TIM_Gen(self):
        pass

    def WDG_Gen(self):
        pass

    def Generate_Hardware(self):
        if not self.DEVICES:
            return

        os.makedirs("output/Hardware", exist_ok=True)
        output = os.path.join("output/Hardware", 'Cyber.v')
        with open(output, 'w') as f:
            # 基础组件
            # TOP
            with open("GUI/demo/Hardware/Cyber.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("Murax.v has been added to the SoC")
            # JTAG
            with open("GUI/demo/Hardware/Cyber.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("JtagBridge.v has been added to the SoC")
            # VexRiscv
            with open("GUI/demo/Hardware/VexRiscv.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("VexRiscv.v has been added to the SoC")
            # APB3 BUS
            with open("GUI/demo/Hardware/APB3BUS.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("APB3BUS.v has been added to the SoC")
            # RAM
            with open("GUI/demo/Hardware/APB3RAM.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("RAM.v has been added to the SoC")

            # Device 生成
            if self.DEVICES["GPIO"] != {}:
                self.GPIO_Gen()
                # with open("demo/Hardware/APB3GPIO.v", 'r', encoding='utf-8') as infile:
                #     f.write(infile.read()+"\n")
                #     print("APB3GPIO.v has been added to the SoC")

                # GPIO 连接
                # if self.DEVICES["UART"] != {}:
                #     with open("demo/Hardware/APB3USART.v", 'r', encoding='utf-8') as infile:
                #         f.write(infile.read()+"\n")
                #         print("APB3USART.v has been added to the SoC")
                # if self.DEVICES["SPI"] != {}:
                #     with open("demo/Hardware/APB3SPI.v", 'r', encoding='utf-8') as infile:
                #         f.write(infile.read()+"\n")
                #         print("APB3SPI.v has been added to the SoC")
                # if self.DEVICES["I2C"] != {}:
                #     with open("demo/Hardware/APB3I2C.v", 'r', encoding='utf-8') as infile:
                #         f.write(infile.read()+"\n")
                #         print("APB3I2C.v has been added to the SoC")
                # if self.DEVICES["TIM"] != {}:
                #     with open("demo/Hardware/APB3TIM.v", 'r', encoding='utf-8') as infile:
                #         f.write(infile.read()+"\n")
                #         print("APB3TIM.v has been added to the SoC")
                # if self.DEVICES["WDG"] != []:
                #     with open("demo/Hardware/APB3WDG.v", 'r', encoding='utf-8') as infile:
                #         f.write(infile.read()+"\n")
                #         print("APB3WDG.v has been added to the SoC")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NewPro()
    dialog.exec_()


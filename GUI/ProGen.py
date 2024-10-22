import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QDialog
from GPIOConf import GPIOConf

class SocGen():
    def __init__(self):
        self.DEVICES = {}
        self.GPIOConf = GPIOConf()

    def GPIO_Config(self):
        if self.GPIOConf.exec_() == QDialog.Accepted:  # QDialog.Accepted 若用户点击了确定按钮
            self.DEVICES = self.GPIOConf.DEVICES
            # 生成 SoC 代码
            self.Generate_Hardware()
            # 生成 Libs
            self.Generate_Software()

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

        # 顶层连接
        self.Top_Connection_Gen()

        os.makedirs("output/Hardware", exist_ok=True)
        output = os.path.join("output/Hardware", 'Cyber.v')
        with open(output, 'w') as f:
            # 基础组件
            # TOP
            with open("demo/Hardware/Murax.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("Murax.v has been added to the SoC")
            # JTAG
            with open("demo/Hardware/JtagBridge.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("JtagBridge.v has been added to the SoC")
            # VexRiscv
            with open("demo/Hardware/VexRiscv.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("VexRiscv.v has been added to the SoC")
            # APB3 BUS
            with open("demo/Hardware/APB3BUS.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("APB3BUS.v has been added to the SoC")
            # RAM
            with open("demo/Hardware/RAM.v", 'r', encoding='utf-8') as infile:
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

    def Generate_Software(self):
        if not self.DEVICES:
            return
        # 输出目录
        os.makedirs("output/Software", exist_ok=True)

        # 复制软件工程模板
        for item in os.listdir("demo/Software"):
            src_path = os.path.join("demo/Software", item)
            dst_path = os.path.join("output/Software", item)
            # 如果是文件，复制文件
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
            # 如果是文件夹，递归复制整个文件夹
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)

        self.Generate_BSP()

    def Generate_BSP(self):
        GPIO_STR = ""
        UART_STR = ""
        SPI_STR = ""
        I2C_STR = ""
        TIM_STR = ""
        WDG_STR = ""

        if self.DEVICES["GPIO"] != {}:
            GPIO_BASE = "APBPERIPH_BASE + 0x00000"
            GPIO_STR += "/*!< GPIO */\n"
            GPIO_STR += '#include "gpio.h"\n'
            GPIO_STR += f"#define GPIO_BASE {GPIO_BASE}\n"
            for GPIO_port, _ in self.DEVICES["GPIO"].items():
                index = ''.join(str(ord(char) - ord('A')) for char in GPIO_port if 'A' <= char <= 'Z')
                GPIO_STR += f"#define GPIO{GPIO_port}_BASE (GPIO_BASE + 0x{index}000)\n"
                GPIO_STR += f"#define GPIO{GPIO_port} ((GPIO_TypeDef *) GPIO{GPIO_port}_BASE)\n"
        if self.DEVICES["UART"] != {}:
            UART_BASE = "APBPERIPH_BASE + 0x10000"
            UART_STR += "/*!< UART */\n"
            UART_STR += '#include "uart.h"\n'
            UART_STR += f"#define UART_BASE {UART_BASE}\n"
            for UART_port, _ in self.DEVICES["UART"].items():
                UART_STR += f"#define UART{UART_port}_BASE (UART_BASE + 0x{UART_port}000)\n"
                UART_STR += f"#define UART{UART_port} ((UART_TypeDef *) UART{UART_port}_BASE)\n"
        if self.DEVICES["SPI"] != {}:
            SPI_BASE = "APBPERIPH_BASE + 0x20000"
            SPI_STR += "/*!< SPI */\n"
            SPI_STR += '#include "spi.h"\n'
            SPI_STR += f"#define SPI_BASE {SPI_BASE}\n"
            for SPI_port, _ in self.DEVICES["SPI"].items():
                SPI_STR += f"#define SPI{SPI_port}_BASE (SPI_BASE + 0x{SPI_port}000)\n"
                SPI_STR += f"#define SPI{SPI_port} ((SPI_TypeDef *) SPI{SPI_port}_BASE)\n"
        if self.DEVICES["I2C"] != {}:
            I2C_BASE = "APBPERIPH_BASE + 0x30000"
            I2C_STR += "/*!< I2C */\n"
            I2C_STR += '#include "i2c.h"\n'
            I2C_STR += f"#define I2C_BASE {I2C_BASE}\n"
            for I2C_port, _ in self.DEVICES["I2C"].items():
                I2C_STR += f"#define I2C{I2C_port}_BASE (I2C_BASE + 0x{I2C_port}000)\n"
                I2C_STR += f"#define I2C{I2C_port} ((I2C_TypeDef *) I2C{I2C_port}_BASE)\n"
        if self.DEVICES["TIM"] != {}:
            TIM_BASE = "APBPERIPH_BASE + 0x40000"
            TIM_STR += "/*!< TIM */\n"
            TIM_STR += '#include "tim.h"\n'
            TIM_STR += f"#define TIM_BASE {TIM_BASE}\n"
            for TIM_port, _ in self.DEVICES["TIM"].items():
                TIM_STR += f"#define TIM{TIM_port}_BASE (TIM_BASE + 0x{TIM_port}000)\n"
                TIM_STR += f"#define TIM{TIM_port} ((TIM_TypeDef *) TIM{TIM_port}_BASE)\n"
        if self.DEVICES["WDG"] != {}:
            WDG_BASE = "APBPERIPH_BASE + 0x50000"
            WDG_STR += "/*!< WDG */\n"
            WDG_STR += '#include "wdg.h"\n'
            WDG_STR += f"#define WDG_BASE {WDG_BASE}\n"
            for WDG_port, state in self.DEVICES["WDG"].items():
                if (WDG_port == "IWDG") & state:
                    WDG_STR += f"#define {WDG_port}_BASE (WDG_BASE + 0x{UART_port}000)\n"
                    WDG_STR += f"#define {WDG_port} ((WDG_TypeDef *) {WDG_port}_BASE)\n"
                elif (WDG_port == "WWDG") & state:
                    WDG_STR += f"#define {WDG_port}_BASE (WDG_BASE + 0x{UART_port}000)\n"
                    WDG_STR += f"#define {WDG_port} ((WWDG_TypeDef *) {WDG_port}_BASE)\n"

        print(GPIO_STR)
        print(UART_STR)
        print(SPI_STR)
        print(I2C_STR)
        print(TIM_STR)
        print(WDG_STR)

        # 读取模板BSP文件内容
        # with open("output/Software/libs/murax.h", 'r', encoding='utf-8') as file:
        #     file_data = file.read()


if __name__ == "__main__":
    # 删除输出目录中的所有内容
    if os.path.exists("output"):
        shutil.rmtree("output")  # 删除整个文件夹及其内容
    # 重新创建该文件夹
    os.makedirs("output", exist_ok=True)

    # 启动 Qt 应用
    app = QApplication(sys.argv)
    Soc_Generate = SocGen()

    # GPIO 配置
    Soc_Generate.GPIO_Config()

    sys.exit()

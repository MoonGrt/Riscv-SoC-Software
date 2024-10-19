import sys, os
from PyQt5.QtWidgets import QApplication
from GPIOConf import GPIOConf

class SocGen():
    def __init__(self):
        self.GPIOS = {}
        self.DEVICES = {}
        self.GPIOConf = GPIOConf()

    def GPIO_Config(self):
        self.GPIOConf.exec_()
        self.GPIOS = self.GPIOConf.gpio_config
        self.DEVICES = self.GPIOConf.DEVICES

    def Top_Connection_Gen(self):
        Connection = ""
        for GPIO_port, AFIO in self.GPIOS.items():
            AFIO_connection = ""
            for i, pin in enumerate(reversed(AFIO)):
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

    def Generate_SoC_Code(self):
        # print(self.GPIOS)
        # print(self.DEVICES)

        if not self.GPIOS or not self.DEVICES:
            return

        self.Top_Connection_Gen()

        # output = os.path.join("", 'SoC.v')
        # with open(output, 'w') as f:
        #     with open("demo/V/Murax.v", 'r', encoding='utf-8') as infile:
        #         f.write(infile.read()+"\n")
        #     print("Murax.v has been added to the SoC")

        #     if self.device["UART"] != []:
        #         with open("demo/V/APB3USART.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3USART.v has been added to the SoC")
        #     if self.device["SPI"] != []:
        #         with open("demo/V/APB3SPI.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3SPI.v has been added to the SoC")
        #     if self.device["I2C"] != []:
        #         with open("demo/V/APB3I2C.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3I2C.v has been added to the SoC")
        #     if self.device["TIM"] != []:
        #         with open("demo/V/APB3TIM.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3TIM.v has been added to the SoC")
        #     if self.device["WDG"] != []:
        #         with open("demo/V/APB3WDG.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3WDG.v has been added to the SoC")

    def Generate_Libs(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Soc_Generate = SocGen()

    # GPIO 配置
    Soc_Generate.GPIO_Config()
    # 生成 SoC 代码
    Soc_Generate.Generate_SoC_Code()
    # 生成 Libs
    Soc_Generate.Generate_Libs()

    sys.exit()

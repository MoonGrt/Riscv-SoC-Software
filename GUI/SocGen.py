import sys, os, shutil
from PyQt5.QtWidgets import QApplication
from GPIOConf import GPIOConf

class SocGen():
    def __init__(self):
        self.GPIOS = {}
        self.DEVICES = {}
        self.GPIOConf = GPIOConf()

    def GPIO_Config(self):
        self.GPIOConf.exec ()
        self.GPIOS = self.GPIOConf.gpio_config
        self.DEVICES = self.GPIOConf.DEVICES

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
        if not self.GPIOS or not self.DEVICES:
            return

        # 顶层连接
        self.Top_Connection_Gen()

        os.makedirs("output/Hardware", exist_ok=True)
        output = os.path.join("output/Hardware", 'SoC.v')
        with open(output, 'w') as f:
            with open("demo/Hardware/Murax.v", 'r', encoding='utf-8') as infile:
                f.write(infile.read()+"\n")
            print("Murax.v has been added to the SoC")

        #     if self.device["UART"] != []:
        #         with open("demo/Hardware/APB3USART.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3USART.v has been added to the SoC")
        #     if self.device["SPI"] != []:
        #         with open("demo/Hardware/APB3SPI.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3SPI.v has been added to the SoC")
        #     if self.device["I2C"] != []:
        #         with open("demo/Hardware/APB3I2C.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3I2C.v has been added to the SoC")
        #     if self.device["TIM"] != []:
        #         with open("demo/Hardware/APB3TIM.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3TIM.v has been added to the SoC")
        #     if self.device["WDG"] != []:
        #         with open("demo/Hardware/APB3WDG.v", 'r', encoding='utf-8') as infile:
        #             f.write(infile.read()+"\n")
        #             print("APB3WDG.v has been added to the SoC")

    def Generate_Software(self):
        # 输出目录
        os.makedirs("output/Software", exist_ok=True)

        # 复制 Makefile
        shutil.copy("demo/Software/makefile", "output/Software/")
        print("Makefile has been added")
        # 复制 linker script
        shutil.copy("demo/Software/linker.ld", "output/Software/")
        print("linker.ld has been added")

        # 生成 demo
        self.Generate_Demo()

        # 根据设备复制 lib 文件
        self.Generate_Libs()

    # 生成 demo
    def Generate_Demo(self):
        # 复制 demo
        os.makedirs("output/Software/src", exist_ok=True)
        shutil.copy("demo/Software/src/main.c", "output/Software/src/")
        print("main.c has been added")

    # 生成 libs
    def Generate_Libs(self):
        if not self.GPIOS or not self.DEVICES:
            return

        # 输出目录
        os.makedirs("output/Software/libs", exist_ok=True)

        # 复制 Murax 库
        shutil.copy("demo/Software/libs/init.S", "output/Software/libs/")  # 复制 startup 文件
        shutil.copy("demo/Software/libs/murax.h", "output/Software/libs/")
        print("Murax libs has been added")

        # 根据设备复制 lib 文件
        if self.DEVICES["GPIO"] != []:
            # 生成 GPIO 库
            shutil.copy("demo/Software/libs/gpio.c", "output/Software/libs/")
            shutil.copy("demo/Software/libs/gpio.h", "output/Software/libs/")
            print("gpio libs has been added")

            # 生成 USART SPI I2C TIM WDG 库
            if self.DEVICES["UART"] != []:
                shutil.copy("demo/Software/libs/usart.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/usart.h", "output/Software/libs/")
                shutil.copy("demo/Software/libs/stdlib.c", "output/Software/libs/")  # 支持 printf
                print("usart libs has been added")
            if self.DEVICES["SPI"] != []:
                shutil.copy("demo/Software/libs/spi.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/spi.h", "output/Software/libs/")
                print("spi libs has been added")
            if self.DEVICES["I2C"] != []:
                shutil.copy("demo/Software/libs/i2c.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/i2c.h", "output/Software/libs/")
                print("i2c libs has been adde")
            if self.DEVICES["TIM"] != []:
                shutil.copy("demo/Software/libs/tim.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/tim.h", "output/Software/libs/")
                print("tim libs has been added")
            if self.DEVICES["WDG"] != []:
                shutil.copy("demo/Software/libs/iwdg.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/iwdg.h", "output/Software/libs/")
                print("iwdg libs has been added")
                shutil.copy("demo/Software/libs/wwdg.c", "output/Software/libs/")
                shutil.copy("demo/Software/libs/wwdg.h", "output/Software/libs/")
                print("wwdg libs has been added")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    Soc_Generate = SocGen()

    # GPIO 配置
    Soc_Generate.GPIO_Config()

    # 输出目录
    os.makedirs("output", exist_ok=True)
    # 生成 SoC 代码
    Soc_Generate.Generate_Hardware()
    # 生成 Libs
    Soc_Generate.Generate_Software()

    sys.exit()

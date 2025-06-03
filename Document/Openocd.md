
ubuntu 编译安装　openocd（支持cmsis-dap）
https://blog.csdn.net/eastgeneral/article/details/84873061

## 一.	Installing libraries and tools Dependency
sudo apt-get install autotools-dev make libtool pkg-config autoconf automake texinfo libudev1 libudev-dev libusb-1.0-0-dev libfox-1.6-dev
报错：
“libudev-dev : Depends: libudev1 (= 245.4-4ubuntu3.20) but 245.4-4ubuntu3.24 is to be installed“

安装指定版本的依赖
sudo apt install libudev1=245.4-4ubuntu3.20

## 二.	Installing HIDAPI
cd ~/
git clone https://github.com/signal11/hidapi.git
cd hidapi/
./bootstrap
./configure
make
sudo make install
nano ~/.profile （添加：PATH="$HOME/bin:/usr/local/lib:$PATH"）
sudo ldconfig
cd ~/
sudo rm -R hidapi

## 三.	Installing OpenOCD
cd ~/openocd_riscv
./bootstrap  # 注意子仓库的拉取
./configure --enable-cmsis-dap
make

## 报错 “fatal error: yaml.h: No such file or directory“
sudo apt update
sudo apt install libyaml-dev

## 四.	Adding udev rule
lsusb
sudo nano /etc/udev/rules.d/CMSIS.rules
```
KERNEL=="hidraw*", ATTRS{idVendor}=="0d28", ATTRS{idProduct}=="0204", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0d28", MODE="0666"
SUBSYSTEM=="usb_device", ATTRS{idVendor}=="0d28", MODE="0666"
```

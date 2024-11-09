import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import os
import signal
from PyQt5.QtCore import QTimer  # 导入 QTimer 用于延时

class ConnectDisconnectApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.openocd_process = None  # 用于保存 openocd 进程

    def initUI(self):
        # 创建两个按钮
        self.connect_button = QPushButton('连接', self)
        self.disconnect_button = QPushButton('断开', self)

        # 连接信号与槽
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button.clicked.connect(self.disconnect)

        # 创建标签显示状态
        self.status_label = QLabel('当前状态：未连接', self)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        
        self.setWindowTitle('连接与断开')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def connect(self):
        if self.openocd_process is None:
            self.status_label.setText('连接中...')
            # 延时 2 秒后执行连接操作
            QTimer.singleShot(2000, self.start_openocd)
        else:
            self.status_label.setText('openocd 已在后台运行')

    def start_openocd(self):
        try:
            # 运行 openocd 并将其放入后台
            self.openocd_process = subprocess.Popen(
                ['/home/moon/openocd_riscv/src/openocd', '-f', '/mnt/hgfs/share/Riscv-SoC-Software/scripts/cyber.cfg'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp
            )
            self.status_label.setText('当前状态：已连接')
        except Exception as e:
            self.status_label.setText(f'连接失败: {str(e)}')

    def disconnect(self):
        if self.openocd_process is not None:
            self.status_label.setText('断开中...')
            # 延时 2 秒后执行断开操作
            QTimer.singleShot(2000, self.stop_openocd)
        else:
            self.status_label.setText('没有运行 openocd')

    def stop_openocd(self):
        try:
            # 结束 openocd 进程
            os.killpg(os.getpgid(self.openocd_process.pid), signal.SIGTERM)
            self.openocd_process = None
            self.status_label.setText('当前状态：已断开')
        except Exception as e:
            self.status_label.setText(f'断开失败: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConnectDisconnectApp()
    sys.exit(app.exec_())

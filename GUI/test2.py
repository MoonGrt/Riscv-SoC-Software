import sys
import pexpect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextBrowser
from PyQt5.QtCore import QThread, pyqtSignal

class GdbBurnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.gdb_thread = None
        self.gdb_process = None

    def initUI(self):
        # 创建界面
        self.setWindowTitle('RISC-V 烧录工具')
        self.setGeometry(300, 300, 500, 300)

        # 创建布局
        layout = QVBoxLayout()

        # 创建标签
        self.label = QLabel('点击按钮进行烧录', self)
        layout.addWidget(self.label)

        # 创建开始烧录按钮
        self.btnBurn = QPushButton('开始烧录', self)
        self.btnBurn.clicked.connect(self.start_burning)
        layout.addWidget(self.btnBurn)

        # 创建停止按钮
        self.btnStop = QPushButton('停止运行', self)
        self.btnStop.clicked.connect(self.stop_running)
        self.btnStop.setEnabled(False)  # 默认禁用停止按钮
        layout.addWidget(self.btnStop)

        # 创建文本浏览器用于显示 GDB 消息
        self.textBrowser = QTextBrowser(self)
        layout.addWidget(self.textBrowser)

        # 设置布局
        self.setLayout(layout)

    def start_burning(self):
        """ 当按钮被点击时，开始烧录过程 """
        self.label.setText('烧录中...')
        self.btnBurn.setEnabled(False)
        self.btnStop.setEnabled(True)

        # 启动烧录的线程
        self.gdb_thread = GdbThread(self)
        self.gdb_thread.progress_signal.connect(self.update_status)
        self.gdb_thread.finished.connect(self.on_finish)
        self.gdb_thread.start()

    def stop_running(self):
        """ 当点击停止按钮时，停止 GDB 运行 """
        if self.gdb_thread:
            self.gdb_thread.terminate('kill')  # 向 GDB 发送 kill 命令
        self.label.setText('运行已停止')
        self.btnStop.setEnabled(False)
        self.btnBurn.setEnabled(True)

    def update_status(self, message):
        """ 更新界面上的状态，并显示 GDB 输出 """
        self.textBrowser.append(message)

    def on_finish(self):
        """ 烧录完成后恢复按钮状态 """
        self.btnStop.setEnabled(False)
        self.btnBurn.setEnabled(True)

class GdbThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.gdb_process = None

    def run(self):
        """ 在子线程中执行 GDB 操作 """
        try:
            # 启动 gdb 进程
            self.gdb_process = pexpect.spawn('/opt/riscv/bin/riscv64-unknown-elf-gdb')
            self._capture_output()  # 捕获并显示输出

            # 输入文件路径
            self.gdb_process.sendline('file /mnt/hgfs/share/Riscv-SoC-Software/projects/rt-thread/test/build/test.elf')
            self._capture_output()

            # 连接远程目标
            self.gdb_process.sendline('target extended-remote :3333')
            self._capture_output()

            # 执行监控命令
            self.gdb_process.sendline('monitor reset halt')
            self._capture_output()

            # 加载程序
            self.gdb_process.sendline('load')
            self._capture_output()

            # 继续执行
            self.gdb_process.sendline('continue')
            self._capture_output()

            # 更新界面为烧录成功
            self.progress_signal.emit('烧录成功！')

            # 进入 GDB 交互模式，直到停止
            self.gdb_process.interact()

        except Exception as e:
            self.progress_signal.emit(f'烧录失败: {str(e)}')
            self.gdb_process.terminate()

    def _capture_output(self):
        """ 捕获 GDB 的输出并发送到 UI """
        try:
            # 捕获 GDB 输出直到遇到 '(gdb)' 提示符
            while True:
                index = self.gdb_process.expect(['\n', '(gdb)'], timeout=5)
                if index == 0:  # 如果捕获到新的一行输出
                    output = self.gdb_process.before.decode('utf-8').strip()
                    if output:
                        self.progress_signal.emit(output)  # 更新 UI
                if index == 1:  # 如果遇到 gdb 提示符
                    break
        except pexpect.TIMEOUT:
            self.progress_signal.emit("GDB 超时，未能获取输出")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GdbBurnerApp()
    ex.show()
    sys.exit(app.exec_())

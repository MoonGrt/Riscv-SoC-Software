from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("复选功能按钮示例")
        self.setGeometry(100, 100, 400, 200)

        # 大小写区分按钮
        self.case_sensitive = QPushButton("", self)
        self.case_sensitive.setIcon(QIcon("icons/case_sensitive.svg"))  # 设置图标
        self.case_sensitive.setCheckable(True)  # 按钮可切换状态
        self.case_sensitive.setGeometry(50, 50, 200, 40)
        self.case_sensitive.setStyleSheet("QPushButton { text-align: left; padding-left: 8px; }")

        # 全字匹配按钮
        self.whole_word = QPushButton("", self)
        self.whole_word.setIcon(QIcon("icons/whole_word_match.svg"))  # 设置图标
        self.whole_word.setCheckable(True)  # 按钮可切换状态
        self.whole_word.setGeometry(50, 100, 200, 40)
        self.whole_word.setStyleSheet("QPushButton { text-align: left; padding-left: 8px; }")

        # 信号连接
        self.case_sensitive.clicked.connect(self.toggle_case_sensitive)
        self.whole_word.clicked.connect(self.toggle_whole_word)

    def toggle_case_sensitive(self):
        if self.case_sensitive.isChecked():
            print("区分大小写: 开启")
        else:
            print("区分大小写: 关闭")

    def toggle_whole_word(self):
        if self.whole_word.isChecked():
            print("全字匹配: 开启")
        else:
            print("全字匹配: 关闭")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

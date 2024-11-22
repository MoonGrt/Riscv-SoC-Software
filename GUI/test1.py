from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout,
    QDialog, QPushButton, QLabel, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextCursor, QIcon
import re


class SearchDialog(QDialog):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit
        self.setWindowTitle("搜索")
        self.init_ui()

    def init_ui(self):
        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white; border: 1px solid gray;")

        # 创建组件
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("搜索...")

        self.case_sensitive = QCheckBox("区分大小写", self)
        self.case_sensitive.setStyleSheet("QCheckBox { border: none; background: none; }")

        self.whole_word = QCheckBox("全字匹配", self)
        self.whole_word.setStyleSheet("QCheckBox { border: none; background: none; }")

        # 创建按钮并设置图标
        self.search_forward_button = QPushButton(self)
        self.search_forward_button.setIcon(QIcon('icons/forward.svg'))  # 设置图标
        self.search_forward_button.setStyleSheet("border: none; background: none;")  # 移除边框
        self.search_forward_button.setIconSize(QSize(20, 20))  # 设置图标大小
        self.search_backward_button = QPushButton(self)
        self.search_backward_button.setIcon(QIcon('icons/backward.svg'))  # 设置图标
        self.search_backward_button.setStyleSheet("border: none; background: none;")  # 移除边框
        self.search_backward_button.setIconSize(QSize(20, 20))  # 设置图标大小

        # 创建关闭按钮
        self.close_button = QPushButton("×", self)  # ×
        self.close_button.setFixedWidth(30)
        self.close_button.setStyleSheet("border: none; color: red; font-weight: bold; font-size: 20px;")

        # 布局
        layout = QHBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.whole_word)
        layout.addWidget(self.search_forward_button)
        layout.addWidget(self.search_backward_button)
        layout.addWidget(self.close_button)

        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        self.setLayout(layout)

        # 信号槽连接
        self.close_button.clicked.connect(self.close)
        self.search_forward_button.clicked.connect(self.search_forward)
        self.search_backward_button.clicked.connect(self.search_backward)

    def search_forward(self):
        """执行向后搜索"""
        self.search(direction="forward")

    def search_backward(self):
        """执行向前搜索"""
        self.search(direction="backward")

    def search(self, direction):
        """通用搜索逻辑"""
        query = self.search_input.text()
        if not query:
            return

        # 获取文本和光标位置
        content = self.text_edit.toPlainText()
        cursor = self.text_edit.textCursor()
        current_pos = cursor.position()

        # 获取搜索选项
        case_sensitive = self.case_sensitive.isChecked()
        whole_word = self.whole_word.isChecked()

        # 设置查找方向
        if direction == "forward":
            start_pos = current_pos
            search_range = content[start_pos:]
        else:  # backward
            start_pos = 0
            search_range = content[:current_pos]

        # 设置正则表达式选项
        flags = 0 if case_sensitive else re.IGNORECASE
        if whole_word:
            query = rf"\b{re.escape(query)}\b"  # 全字匹配的正则表达式

        # 查找匹配
        match = None
        if direction == "forward":
            match = re.search(query, search_range, flags)
        else:  # backward
            match = list(re.finditer(query, search_range, flags))
            if match:
                match = match[-1]  # 取最后一个匹配项

        # 更新状态和光标
        if match:
            start = match.start() + (current_pos if direction == "forward" else 0)
            end = match.end() + (current_pos if direction == "forward" else 0)

            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)  # 修改为 QTextCursor.KeepAnchor
            self.text_edit.setTextCursor(cursor)

    def closeEvent(self, event):
        """关闭搜索框时将焦点返回到文本编辑器"""
        self.text_edit.setFocus()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("带全字匹配的搜索功能")
        self.resize(800, 600)

        # 主组件
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 示例文本
        self.text_edit.setPlainText(
            "这是一个示例文本，用于展示搜索功能。\n"
            "搜索示例：支持全字匹配、大小写敏感、向前与向后查找。\n"
            "全字匹配的例子：word 与 wordy 不匹配。"
        )

        # 初始化搜索对话框
        self.search_dialog = None

        # 安装事件过滤器
        self.text_edit.installEventFilter(self)

    def eventFilter(self, obj, event):
        """捕获快捷键事件"""
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier:
                self.open_search_dialog()
                return True
        return super().eventFilter(obj, event)

    def open_search_dialog(self):
        """打开搜索对话框"""
        if not self.search_dialog:
            self.search_dialog = SearchDialog(self.text_edit)
        self.search_dialog.show()  # 使用非模态模式
        self.search_dialog.raise_()  # 将对话框置于最前
        self.search_dialog.activateWindow()  # 激活对话框窗口



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

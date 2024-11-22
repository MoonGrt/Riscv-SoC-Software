from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout,
    QDialog, QPushButton, QLabel, QHBoxLayout, QCheckBox, QFileDialog, QAction, QMenuBar, QTabWidget, QWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextCursor, QIcon
import re


class SearchDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 保存主窗口实例
        self.setWindowTitle("搜索")
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white; border: 1px solid gray;")

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("搜索...")

        self.case_sensitive = QCheckBox("区分大小写", self)
        self.case_sensitive.setStyleSheet("QCheckBox { border: none; background: none; }")

        self.whole_word = QCheckBox("全字匹配", self)
        self.whole_word.setStyleSheet("QCheckBox { border: none; background: none; }")

        self.search_forward_button = QPushButton(self)
        self.search_forward_button.setIcon(QIcon('icons/forward.svg'))
        self.search_forward_button.setStyleSheet("border: none; background: none;")
        self.search_forward_button.setIconSize(QSize(20, 20))

        self.search_backward_button = QPushButton(self)
        self.search_backward_button.setIcon(QIcon('icons/backward.svg'))
        self.search_backward_button.setStyleSheet("border: none; background: none;")
        self.search_backward_button.setIconSize(QSize(20, 20))

        self.close_button = QPushButton("×", self)
        self.close_button.setFixedWidth(30)
        self.close_button.setStyleSheet("border: none; color: red; font-weight: bold; font-size: 20px;")

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

        self.close_button.clicked.connect(self.close)
        self.search_forward_button.clicked.connect(self.search_forward)
        self.search_backward_button.clicked.connect(self.search_backward)

    def search_forward(self):
        self.search(direction="forward")

    def search_backward(self):
        self.search(direction="backward")

    def search(self, direction):
        query = self.search_input.text()
        if not query:
            return

        # 获取当前活动标签页的 QTextEdit
        current_text_edit = self.main_window.tab_widget.currentWidget()
        if not current_text_edit:
            return

        content = current_text_edit.toPlainText()
        cursor = current_text_edit.textCursor()
        current_pos = cursor.position()

        case_sensitive = self.case_sensitive.isChecked()
        whole_word = self.whole_word.isChecked()

        if direction == "forward":
            start_pos = current_pos
            search_range = content[start_pos:]
        else:
            start_pos = 0
            search_range = content[:current_pos]

        flags = 0 if case_sensitive else re.IGNORECASE
        if whole_word:
            query = rf"\b{re.escape(query)}\b"

        match = None
        if direction == "forward":
            match = re.search(query, search_range, flags)
        else:
            match = list(re.finditer(query, search_range, flags))
            if match:
                match = match[-1]

        if match:
            start = match.start() + (current_pos if direction == "forward" else 0)
            end = match.end() + (current_pos if direction == "forward" else 0)

            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            current_text_edit.setTextCursor(cursor)

    def closeEvent(self, event):
        self.main_window.tab_widget.currentWidget().setFocus()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多页面编辑器")
        self.resize(800, 600)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.new_file()

        self.search_dialog = None
        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('文件')

        new_action = QAction('新建文件', self)
        open_action = QAction('打开文件', self)
        save_action = QAction('保存文件', self)
        exit_action = QAction('退出', self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        # 添加搜索快捷键
        search_action = QAction('搜索', self)
        search_action.setShortcut('Ctrl+F')
        search_action.triggered.connect(self.open_search_dialog)
        menubar.addAction(search_action)

    def new_file(self):
        text_edit = QTextEdit(self)
        self.tab_widget.addTab(text_edit, "新建文件")
        self.tab_widget.setCurrentWidget(text_edit)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '所有文件 (*)')
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                text_edit = QTextEdit(self)
                text_edit.setPlainText(content)
                self.tab_widget.addTab(text_edit, file_name.split("/")[-1])
                self.tab_widget.setCurrentWidget(text_edit)

    def save_file(self):
        current_tab = self.tab_widget.currentWidget()
        file_name, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '所有文件 (*)')
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(current_tab.toPlainText())

    def open_search_dialog(self):
        if not self.search_dialog:
            self.search_dialog = SearchDialog(self)
        self.search_dialog.show()  # 打开搜索对话框
        self.search_dialog.raise_()  # 将对话框置于最前
        self.search_dialog.activateWindow()  # 激活对话框窗口

    def closeEvent(self, event):
        self.tab_widget.currentWidget().setFocus()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

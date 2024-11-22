import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QFileDialog, QTextEdit, QAction, QMenuBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont('Courier', 10))
        self.setTabStopDistance(40)
        self.setAcceptRichText(False)  # 禁用富文本模式

    def comment_code(self):
        cursor = self.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:  # 如果有选中的文本
            # 获取选中文本中的每一行，逐行注释
            lines = selected_text.split('\n')
            line_number = cursor.blockNumber()  # 获取当前选中区域的起始行号
            for idx, line in enumerate(lines):
                self.comment_current_line(line_number + idx)  # 逐行调用注释，传递行号
        else:
            # 没有选中文本时，注释光标所在行
            line_number = cursor.blockNumber()  # 获取光标所在行号
            self.comment_current_line(line_number)

    def comment_current_line(self, line_number):
        cursor = self.textCursor()

        # 将光标移动到指定的行号
        cursor.movePosition(cursor.StartOfDocument)
        cursor.movePosition(cursor.NextBlock, mode=cursor.KeepAnchor)  # 先选中第一行
        for _ in range(line_number):  # 跳转到指定的行
            cursor.movePosition(cursor.NextBlock, mode=cursor.KeepAnchor)

        # 获取该行的文本
        selected_text = cursor.selectedText()

        # 获取当前行的前导空格
        leading_whitespace = self.get_leading_whitespace(selected_text)

        if selected_text.strip().startswith("//"):  # 如果已经是注释，则取消注释
            cursor.removeSelectedText()
            cursor.insertText(leading_whitespace + selected_text.lstrip("//").strip())
        else:  # 否则添加注释
            cursor.removeSelectedText()
            cursor.insertText(leading_whitespace + "// " + selected_text.strip())

        self.setTextCursor(cursor)

    def get_leading_whitespace(self, line):
        """ 获取行首的空白字符（空格或制表符） """
        return ' ' * (len(line) - len(line.lstrip()))


class CodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Multi-tab Code Editor')
        self.setGeometry(100, 100, 800, 600)

        # 设置主页面为QTabWidget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 菜单栏
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")

        # 文件菜单
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(save_action)

        close_action = QAction("Close", self)
        close_action.setShortcut(QKeySequence("Ctrl+W"))
        close_action.triggered.connect(self.close_file)
        self.file_menu.addAction(close_action)

        # 编辑菜单
        comment_action = QAction("Comment/Uncomment", self)
        comment_action.setShortcut(QKeySequence("Ctrl+/"))
        comment_action.triggered.connect(self.comment_code)
        self.edit_menu.addAction(comment_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "C Files (*.c);;Text Files (*.txt);;All Files (*)")
        if file_path:
            editor = CodeEditor()
            with open(file_path, 'r', encoding='utf-8') as file:
                editor.setPlainText(file.read())
            self.tabs.addTab(editor, file_path.split('/')[-1])

    def save_file(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "C Files (*.c);;Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(current_widget.toPlainText())

    def close_file(self):
        current_index = self.tabs.currentIndex()
        self.tabs.removeTab(current_index)

    def comment_code(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            current_widget.comment_code()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeEditorWindow()
    window.show()
    sys.exit(app.exec_())

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

        if selected_text:  # 有选中的文本
            self.comment_selected_text(selected_text)
        else:
            # 如果没有选中文本，就注释当前行
            self.comment_current_line()

    def comment_current_line(self):
        cursor = self.textCursor()
        cursor.select(cursor.LineUnderCursor)  # 选中当前行
        selected_text = cursor.selectedText()

        # 获取当前行的前导空格
        leading_whitespace = self.get_leading_whitespace(selected_text)
        
        if selected_text.strip().startswith("//"):  # 如果已经是注释，则取消注释
            cursor.removeSelectedText()
            cursor.insertText(leading_whitespace + selected_text.lstrip(" //").strip())
        else:  # 否则添加注释
            cursor.removeSelectedText()
            cursor.insertText(leading_whitespace + "// " + selected_text.strip())

        self.setTextCursor(cursor)

    def comment_selected_text(self, selected_text):
        cursor = self.textCursor()
        cursor.select(cursor.Document)  # 选中所有文本
        lines = selected_text.split('\n')

        commented_lines = []
        for line in lines:
            # 获取每一行的前导空格
            leading_whitespace = self.get_leading_whitespace(line)
            if line.strip().startswith("//"):  # 如果已经是注释，取消注释
                commented_lines.append(leading_whitespace + line.lstrip("//").strip())
            else:  # 否则添加注释
                commented_lines.append(leading_whitespace + "// " + line.strip())

        cursor.removeSelectedText()
        cursor.insertText("\n".join(commented_lines))
        self.setTextCursor(cursor)

    def get_leading_whitespace(self, line):
        """ 获取行首的空白字符（空格或制表符） """
        return ' ' * (len(line) - len(line.lstrip()))

    def remove_block_comment(self):
        cursor = self.textCursor()
        cursor.select(cursor.Document)  # 选中所有文本
        selected_text = cursor.selectedText()

        # 如果已经是多行注释，则去掉块注释
        if selected_text.strip().startswith('/*') and selected_text.strip().endswith('*/'):
            lines = selected_text.split('\n')
            uncommented_lines = [line.strip('/* ').strip() for line in lines if not line.strip().startswith('/*')]
            cursor.removeSelectedText()
            cursor.insertText("\n".join(uncommented_lines))
            self.setTextCursor(cursor)


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
        # 在程序启动时自动打开 test.c 文件
        self.open_default_file()

    def open_default_file(self):
        """默认打开 test.c 文件"""
        default_file = "test.c"  # 设置默认文件路径
        try:
            with open(default_file, 'r', encoding='utf-8') as file:
                editor = CodeEditor()
                editor.setPlainText(file.read())
                self.tabs.addTab(editor, default_file)
        except FileNotFoundError:
            print(f"默认文件 {default_file} 未找到。")

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

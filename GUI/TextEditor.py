import sys, os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,
                             QVBoxLayout, QWidget, QTreeView, QFileSystemModel, QSplitter, QStyledItemDelegate)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal

class RowColorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 设置奇偶行颜色
        if index.row() % 2 == 0:
            painter.fillRect(option.rect, QColor("#A68F8B"))  # 偶数行颜色
        else:
            painter.fillRect(option.rect, QColor("#D1A7A4"))  # 奇数行颜色
        super().paint(painter, option, index)

class TextEditor(QMainWindow):
    fileSelected = pyqtSignal(str)  # 定义一个信号，传递文件路径
    def __init__(self, initial_path=None):
        super().__init__()
        self.initUI(initial_path)

    def initUI(self,initial_path):
        self.textEdit = QTextEdit(self)

        # 设置窗口背景颜色
        self.setStyleSheet("background-color: #C18E93;")  # 刚蓝色

        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Set the root path to be empty
        self.fileTree = QTreeView(self)
        self.fileTree.setModel(self.model)
        self.fileTree.setRootIndex(self.model.index(os.path.expanduser("~")))  # Set initial folder to home
        self.fileTree.setColumnHidden(1, True)  # Hide the size column
        self.fileTree.setColumnHidden(2, True)  # Hide the type column
        self.fileTree.setColumnHidden(3, True)  # Hide the date modified column
        self.fileTree.doubleClicked.connect(self.loadFile)

        # 使用自定义代理设置奇偶行背景颜色
        self.fileTree.setItemDelegate(RowColorDelegate())

        # 设置文本编辑区域背景颜色
        self.textEdit.setStyleSheet("background-color: #CEA69B; color: #000000;")  # 深海蓝色背景，黑色文字


        # 创建垂直分割器
        splitter = QSplitter(Qt.Vertical, self)
        splitter.addWidget(self.fileTree)  # 添加文件树
        # splitter.addWidget(self.textEdit)   # 添加文本编辑区域

        # 设置比例
        # splitter.setSizes([800, 80])  # 800:80 比例（可以根据需要调整）

        # 设置中心窗口
        self.setCentralWidget(splitter)

        self.createActions()
        self.createMenus()

        self.setWindowTitle('文本编辑器')
        self.setGeometry(100, 100, 800, 400)
        if initial_path:
            self.fileTree.setRootIndex(self.model.index(initial_path))  # 打开指定路径

    def createActions(self):
        self.newAction = QAction('新建', self)
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QAction('打开文件夹', self)
        self.openAction.triggered.connect(self.openDirectory)

        self.saveAction = QAction('保存', self)
        self.saveAction.triggered.connect(self.saveFile)

        self.exitAction = QAction('退出', self)
        self.exitAction.triggered.connect(self.close)

    def createMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File Table')

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

    def newFile(self):
        if self.textEdit.document().isModified():
            response = QMessageBox.question(self, '警告', '文件已修改，是否保存？',
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if response == QMessageBox.Yes:
                self.saveFile()
            elif response == QMessageBox.Cancel:
                return
        self.textEdit.clear()

    def openDirectory(self):
        dirName = QFileDialog.getExistingDirectory(self, '打开文件夹', '')
        if dirName:
            self.fileTree.setRootIndex(self.model.index(dirName))

    def loadFile(self, index):
        filePath = self.model.filePath(index)
        if os.path.isfile(filePath):
            with open(filePath, 'r', encoding='utf-8') as file:
                # self.textEdit.setPlainText(file.read())
                 content = file.read()
                 self.textEdit.setPlainText(content)
                 self.fileSelected.emit(filePath)  # 发出信号，传递文件路径

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '文本文件 (*.txt);;所有文件 (*)', options=options)
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())

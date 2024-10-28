import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,
                             QVBoxLayout, QWidget, QTreeView, QFileSystemModel, QSplitter)

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Set the root path to be empty
        self.fileTree = QTreeView(self)
        self.fileTree.setModel(self.model)
        self.fileTree.setRootIndex(self.model.index(os.path.expanduser("~")))  # Set initial folder to home
        self.fileTree.setColumnHidden(1, True)  # Hide the size column
        self.fileTree.setColumnHidden(2, True)  # Hide the type column
        self.fileTree.setColumnHidden(3, True)  # Hide the date modified column
        self.fileTree.doubleClicked.connect(self.loadFile)

        splitter = QSplitter(self)
        splitter.addWidget(self.fileTree)
        splitter.addWidget(self.textEdit)

        self.setCentralWidget(splitter)

        self.createActions()
        self.createMenus()

        self.setWindowTitle('文本编辑器')
        self.setGeometry(100, 100, 800, 400)

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
        fileMenu = menuBar.addMenu('文件')

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
                self.textEdit.setPlainText(file.read())

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

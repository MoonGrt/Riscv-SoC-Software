import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class CustomTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

    def mousePressEvent(self, event):
        # 获取鼠标点击的位置
        pos = event.pos()
        # 获取点击的行
        row = self.rowAt(pos.y())

        # 判断鼠标是否点击在行标题旁边
        if row != -1 and pos.x() < self.verticalHeader().width():
            # 在当前行和上一行之间插入新行
            self.insertRow(row)
            # 选中插入的新行
            self.setCurrentCell(row, 0)

        # 调用基类的 mousePressEvent 方法，保持其他功能正常
        super().mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget Example")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.table_widget = CustomTableWidget(5, 3)  # 5行3列的表格
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

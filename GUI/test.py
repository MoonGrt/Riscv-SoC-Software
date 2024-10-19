import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QColorDialog, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QLinearGradient, QPainter, QColor
from PyQt5.QtCore import Qt

class GradientTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.gradient_color = Qt.blue  # 默认渐变颜色
        self.gradient_cells = [(1, 1)]  # 要设置渐变色的单元格

        # 按钮用于选择颜色
        self.color_button = QPushButton("选择渐变颜色")
        self.color_button.clicked.connect(self.choose_color)
        self.setCellWidget(0, 0, self.color_button)  # 将按钮放在 (0, 0) 单元格

    def choose_color(self):
        color = QColorDialog.getColor()  # 打开颜色选择对话框
        if color.isValid():  # 检查用户是否选择了有效颜色
            self.gradient_color = color  # 更新渐变颜色
            self.update()  # 刷新表格以重绘渐变背景

    def paintEvent(self, event):
        # 先绘制表格的默认背景
        super().paintEvent(event)

        # 创建 QPainter 对象
        painter = QPainter(self.viewport())

        # 遍历要设置渐变色的单元格
        for (row, column) in self.gradient_cells:
            rect = self.visualRect(self.model().index(row, column))  # 获取单元格的矩形区域

            # 创建渐变色
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            gradient.setColorAt(0, QColor("#FCFCFC"))  # 渐变结束色（#FCFCFC）
            gradient.setColorAt(1, self.gradient_color)  # 渐变起始色（用户选择的颜色）

            # 绘制渐变背景
            painter.fillRect(rect, gradient)

            # 绘制单元格的文本
            item = self.item(row, column)
            if item:
                painter.drawText(rect, Qt.AlignCenter, item.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建表格
    table = GradientTableWidget(5, 3)
    for row in range(5):
        for column in range(3):
            table.setItem(row, column, QTableWidgetItem(f"{row}, {column}"))

    table.setWindowTitle("QTableWidget with User-defined Gradient Color")
    table.resize(400, 300)
    table.show()

    sys.exit(app.exec_())

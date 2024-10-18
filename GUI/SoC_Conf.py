import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt

class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__(0, 0)
        # 删除行列标题
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    # 重写鼠标右键点击事件
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # 获取当前点击的单元格位置
            row = self.rowAt(event.pos().y())
            col = self.columnAt(event.pos().x())
            # 检查是否在有效单元格范围内
            if row > 0 and col > 0:
                item = self.item(row, col)
                if item:
                    current_color = item.background().color()
                    # 判断当前单元格背景是否是淡绿色
                    if current_color == QColor('lightgreen'):
                        # 如果是淡绿色，则恢复为默认的白色
                        item.setBackground(QColor('white'))
                    else:
                        # 否则，将其设置为淡绿色
                        item.setBackground(QColor('lightgreen'))
        else:
            # 调用父类的默认行为
            super().mousePressEvent(event)

class GPIOTable(QWidget):
    def __init__(self):
        super().__init__()

        #  初始化变量
        self.dev = {"GPIO": ["GPIOA", "GPIOB"],
                    "UART": ["UART1", "UART2", "UART3"],
                    "SPI": ["SPI1", "SPI2"],
                    "I2C": ["I2C1", "I2C2"],
                    "TIM": ["TIM1", "TIM2", "TIM3", "TIM4"],
                    "WDG": ["IWDG", "WWDG"]}

        self.folded_rows = {}  # 用于跟踪展开/折叠状态
        self.row_indexes = {}  # 用于存储每个设备对应的行索引

        self.init_ui()

    def init_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon("icons/GPIO.svg"))
        # 设置窗口标题和尺寸
        self.setWindowTitle("GPIO Table")
        self.resize(950, 450)  # 窗口大小

        # 创建表格
        self.table = CustomTableWidget()
        # 设置单元格格式
        self.update_table()

        # 创建布局并将表格加入
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_table(self):
        # 重置表格
        self.table.clear()
        self.table.setColumnCount(len(self.dev["GPIO"])*16+1)

        # 第一行
        self.table.insertRow(self.table.rowCount())
        self.set_table_item(0, 0, "", False)
        for j, gpio in enumerate(self.dev["GPIO"]):
            self.table.setSpan(0, 16*j+1, 1, 16)  # 合并单元格
            self.set_table_item(0, 16*j+1, gpio, False)
        # 第二行、第三行
        self.table.insertRow(self.table.rowCount())
        self.table.insertRow(self.table.rowCount())
        for j in range(self.table.columnCount()):
            if j == 0:
                item_row2 = "PIN"
                item_row3 = "AFIO"
            else:
                item_row2 = str((j-1)%16)
                item_row3 = ""
            self.set_table_item(1, j, item_row2, False)
            self.set_table_item(2, j, item_row3, False)

        # 后续行 添加所需组件
        for component in ["UART", "SPI", "I2C", "TIM", "WDG"]:
            self.add_row(component)

        # 设置单元格为正方形
        cell_size = 50  # 设定单元格大小为 50x50 像素
        for i in range(self.table.columnCount()):
            if i == 0:
                self.table.setColumnWidth(i, cell_size * 2)  # 设置列宽为 100 像素
            else:
                self.table.setColumnWidth(i, cell_size)  # 设置列宽
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, cell_size)  # 设置行高

    # 设置单元格内容
    def set_table_item(self, row, column, text, writeable=True):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        if writeable:
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # 设置可编辑
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
        self.table.setItem(row, column, item)

    # 添加行
    def add_row(self, dev):
        # 记录当前设备的行索引
        self.row_indexes[dev] = []

        # 添加新行
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)

        # 创建一个按钮用于折叠/展开
        fold_button = QPushButton(dev)
        fold_button.setCheckable(True)
        fold_button.toggled.connect(lambda checked, device=dev: self.fold_row(device, checked))
        self.table.setCellWidget(current_row, 0, fold_button)
        # 其他行合并
        self.table.setSpan(current_row, 1, 1, self.table.columnCount()-1)
        self.set_table_item(current_row, 1, "", False)  # 设置不可编辑的标签
        current_row += 1

        # 插入项目并记录行索引
        for item in self.dev[dev]:
            self.table.insertRow(current_row)
            self.set_table_item(current_row, 0, item, False)
            for j in range(1, self.table.columnCount()):
                self.set_table_item(current_row, j, "", False)
            self.row_indexes[dev].append(current_row)  # 记录行索引
            current_row += 1

        # self.table.insertRow(current_row)
        # add_button = QPushButton("+")
        # # add_button.toggled.connect(lambda checked, device=dev: self.fold_row(device, checked))
        # self.table.setCellWidget(current_row, 0, add_button)
        # self.row_indexes[dev].append(current_row)

        self.fold_row(dev, False)  # 默认折叠

    def fold_row(self, dev, checked):
        # 获取当前设备的项目行索引
        if dev not in self.row_indexes:
            return

        if checked:  # 如果按钮被检查（展开）
            # 显示项目行
            for row in self.row_indexes[dev]:
                self.table.setRowHidden(row, False)
            self.folded_rows[dev] = False  # 更新状态为展开
        else:  # 如果按钮未被检查（折叠）
            # 隐藏项目行
            for row in self.row_indexes[dev]:
                self.table.setRowHidden(row, True)
            self.folded_rows[dev] = True  # 更新状态为折叠

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIOTable()
    window.show()
    sys.exit(app.exec_())

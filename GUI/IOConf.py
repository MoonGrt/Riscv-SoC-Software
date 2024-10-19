import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QMenu
from PyQt5.QtGui import QIcon, QColor, QFont, QPainter, QLinearGradient
from PyQt5.QtCore import Qt

# 设备
DEVICES = {"GPIO": ["GPIOA", "GPIOB"],
           "UART": ["UART1", "UART2", "UART3"],
           "SPI": ["SPI1", "SPI2"],
           "I2C": ["I2C1", "I2C2"],
           "TIM": ["TIM1", "TIM2", "TIM3", "TIM4"],
           "WDG": ["IWDG", "WWDG"]}

class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__(0, 0)
        self.current_row = None
        self.current_column = None

        # 要设置渐变色的单元格
        self.gradient_cells = []

        # 删除行列标题
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    def paintEvent(self, event):
        # 先绘制表格的默认背景
        super().paintEvent(event)
        # 创建 QPainter 对象
        painter = QPainter(self.viewport())

        # 遍历要设置渐变色的单元格
        for (enable, row, column, color) in self.gradient_cells:
            rect = self.visualRect(self.model().index(row, column))  # 获取单元格的矩形区域
            # 创建渐变色
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            if enable:  # 判断是否启用渐变色
                gradient.setColorAt(0, QColor("#FCFCFC"))  # 渐变结束色（#FCFCFC）
            else:
                gradient.setColorAt(0, QColor(color))  # 渐变起始色（#FFFFFF）
            gradient.setColorAt(1, QColor(color))  # 渐变起始色
            # 绘制渐变背景
            painter.fillRect(rect, gradient)
            # 绘制单元格的文本
            item = self.item(row, column)
            if item:
                painter.drawText(rect, Qt.AlignCenter, item.text())

    # 重写鼠标右键点击事件
    def mousePressEvent(self, event):
        # 获取当前点击的单元格位置
        self.current_row = self.rowAt(event.pos().y())
        self.current_column = self.columnAt(event.pos().x())
        if event.button() == Qt.MiddleButton:
            # 检查是否在有效单元格范围内
            if self.current_row > 0 and self.current_column > 0:
                item = self.item(self.current_row, self.current_column)
                if item:
                    current_color = item.background().color()
                    # 判断当前单元格背景是否是淡绿色
                    if current_color == QColor('lightgreen'):
                        # 如果是淡绿色，则恢复为默认的白色
                        item.setBackground(QColor('white'))
                    else:
                        # 否则，将其设置为淡绿色
                        item.setBackground(QColor('lightgreen'))
        elif event.button() == Qt.RightButton:
            try:
                if self.current_column == 0:
                    return
                device_name = self.item(self.current_row, 0).text()
                self.context_menu(event.pos(), device_name)
            except:
                return
        else:
            # 调用父类的默认行为
            super().mousePressEvent(event)

    def context_menu(self, position, device_name):
        # 根据设备类型创建右键菜单
        device = ''.join(filter(str.isalpha, device_name))  # 提取字母
        num = ''.join(filter(str.isdigit, device_name))   # 提取数字
        if device == "UART":
            menu_list = [f"RX{num}", f"TX{num}", "None"]
        elif device == "SPI":
            menu_list = [f"SCK{num}", f"MISO{num}", f"MOSI{num}", f"CS{num}", "None"]
        elif device == "I2C":
            menu_list = [f"SCL{num}", f"SDA{num}", "None"]
        elif device == "TIM":
            menu_list = [f"T{num}CH1", f"T{num}CH2", f"T{num}CH3", f"T{num}CH4", "None"]
        # 根据设备类型创建右键菜单
        if menu_list:
            self.create_menu(menu_list, position)

    def create_menu(self, menu_list, position):
        # 创建右键菜单并连接信号与槽
        menu = QMenu()
        for text in menu_list:
            menu_action = menu.addAction(text)
            menu_action.triggered.connect(lambda checked, content=text: self.fill_cell(content))
        # 在点击的地方显示菜单
        menu.exec_(self.viewport().mapToGlobal(position))

    # 填充单元格内容
    def fill_cell(self, content):
        if self.current_row is None or self.current_column is None:
            return  # 如果当前行或列为空，直接返回
        if content == "None":
            self.set_item(self.current_row, self.current_column, "", False, "white")
            self.set_item(2, self.current_column, "", False, "white")
        else:
            # 设置单元格内容为有效值
            self.set_item(self.current_row, self.current_column, content, False, "lightgreen")
            self.set_item(2, self.current_column, content, False, "lightgreen")
        # 检查单元格内容是否有效
        item_list, error_list = self.chech_item()
        if item_list or error_list:
            self.update_color(item_list, error_list)

    # 检查单元格内容是否有效
    def chech_item(self):
        row_list = {}
        error_list = []
        item_list = []
        # 遍历表格
        for j in range(self.columnCount() - 1):
            col_list = []
            for i in range(self.rowCount() - 3):
                cell_item = self.item(i + 3, j + 1)
                try:
                    cell_item_text = cell_item.text()
                    if cell_item_text:  # 检查单元格是否有内容
                        if ''.join(filter(str.isalpha, cell_item_text)) in ["RX", "MISO"]:  # 检查是否为输入IO
                            if cell_item_text in row_list:  # 如果列中已有相同的输入IO
                                row_list[cell_item_text].append((i, j))
                            else:
                                row_list[cell_item_text] = [(i, j)]
                        col_list.append((cell_item_text, i))
                except:
                    pass
            if col_list:
                if len(col_list) > 1:  # 如果列中有多个有效值
                    self.set_item(2, j+1, "", False, "red")
                    # error_list.append((2, j+1))
                    for row in col_list:
                        error_list.append((row[1]+3, j+1))
                else:
                    self.set_item(2, j+1, col_list[0][0], False, "red")
                    # item_list.append((2, j+1))
                    for item in col_list:
                        item_list.append((item[1]+3, j+1))
        # 检查引脚定义是否唯一
        for number, indexs in row_list.items():
            if len(indexs) > 1:  # 如果列中有多个有效值
                for index in indexs:
                    error_list.append((2, index[1]+1))
                    error_list.append((index[0]+3, index[1]+1))
        # print(item_list, error_list)
        return item_list, error_list

    # 更新单元格颜色
    def update_color(self, item_list, error_list):
        # 填充渐变色
        self.gradient_cells = []  # 清空单元格颜色
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if (i, j) in item_list:
                    self.gradient_cells.append((True, i, j, "lightgreen"))
                if (i, j) in error_list:
                    self.gradient_cells.append((False, i, j, "red"))

    # 设置单元格内容
    def set_item(self, row, column, text, writeable=True, color=None, font_size=7):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)

        # 设置字体大小
        font = QFont()  # 创建一个字体对象
        font.setPointSize(font_size)  # 设置字体大小
        item.setFont(font)  # 将字体应用于项
        # 设置单元格是否可编辑
        if writeable:
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # 设置可编辑
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
        # 设置单元格
        self.setItem(row, column, item)
        # 设置单元格颜色
        if color:
            self.gradient_cells.append((False, row, column, color))

class GPIOTable(QWidget):
    def __init__(self):
        super().__init__()

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
        self.table.setColumnCount(len(DEVICES["GPIO"])*16+1)

        # 第一行
        self.table.insertRow(self.table.rowCount())
        self.table.set_item(0, 0, "", False, font_size=10)
        for j, gpio in enumerate(DEVICES["GPIO"]):
            self.table.setSpan(0, 16*j+1, 1, 16)  # 合并单元格
            self.table.set_item(0, 16*j+1, gpio, False, font_size=10)
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
            self.table.set_item(1, j, item_row2, False, font_size=10)
            self.table.set_item(2, j, item_row3, False, font_size=10)

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
        self.table.set_item(current_row, 1, "", False, font_size=10)  # 设置不可编辑的标签
        current_row += 1

        # 插入项目并记录行索引
        for item in DEVICES[dev]:
            self.table.insertRow(current_row)
            self.table.set_item(current_row, 0, item, False, font_size=10)
            for j in range(1, self.table.columnCount()):
                self.table.set_item(current_row, j, "", False, font_size=10)
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

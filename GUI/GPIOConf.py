import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout,  QPushButton, QMenu, QDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QColor, QFont, QPainter, QLinearGradient
from PyQt5.QtCore import Qt

class GPIOConfTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 0)
        self.current_row = None
        self.current_column = None

        # 要设置渐变色的单元格
        self.gradient_cells = []

        # 删除行列标题
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    # 重写 paintEvent 函数，实现单元格背景的渐变色
    # def paintEvent(self, event):
    #     # 先绘制表格的默认背景
    #     super().paintEvent(event)
    #     # 创建 QPainter 对象
    #     painter = QPainter(self.viewport())

    #     # 遍历要设置渐变色的单元格
    #     for (enable, row, column, color) in self.gradient_cells:
    #         rect = self.visualRect(self.model().index(row, column))  # 获取单元格的矩形区域
    #         # 创建渐变色
    #         gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
    #         if enable:  # 判断是否启用渐变色
    #             gradient.setColorAt(0, QColor("#FCFCFC"))  # 渐变结束色（#FCFCFC）
    #         else:
    #             gradient.setColorAt(0, QColor(color))  # 渐变起始色（#FFFFFF）
    #         gradient.setColorAt(1, QColor(color))  # 渐变起始色
    #         # 绘制渐变背景
    #         painter.fillRect(rect, gradient)
    #         # 绘制单元格的文本
    #         item = self.item(row, column)
    #         if item:
    #             painter.drawText(rect, Qt.AlignCenter, item.text())

    # 重写鼠标右键点击事件
    def mousePressEvent(self, event):
        # 获取当前点击的单元格位置
        self.current_row = self.rowAt(event.pos().y())
        self.current_column = self.columnAt(event.pos().x())
        if event.button() == Qt.MiddleButton:
            # 检查是否在有效单元格范围内
            item = self.item(self.current_row, self.current_column)
            if item:
                current_color = item.background().color()
                # 判断当前单元格背景是否是淡绿色
                if current_color == QColor('red'):
                    pass
                elif current_color == QColor('lightgreen'):
                    item.setBackground(QColor('white'))  # 如果是淡绿色，则恢复为默认的白色
                else:
                    item.setBackground(QColor('lightgreen'))  # 否则，将其设置为淡绿色
        else:
            # 调用父类的默认行为
            super().mousePressEvent(event)

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
            # self.gradient_cells.append((False, row, column, color))
            self.item(row, column).setBackground(QColor(color))


class GPIOConf(QDialog):
# class GPIOConf(QWidget):
    def __init__(self):
        super().__init__()

        self.DEVICES = {"GPIO": ["A"], "UART": [], "SPI": [], "I2C": [], "TIM": [], "WDG": []}  # 设备
        self.gpio_config = {}  # 用于存储GPIO配置
        self.row_indexes = {}  # 用于存储每个设备对应的行索引
        self.row = 0
        self.col = 0

        self.init_ui()

    def init_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon("icons/GPIO.svg"))
        # 设置窗口标题和尺寸
        self.setWindowTitle("GPIO Table")
        self.resize(950, 450)  # 窗口大小

        # 创建表格
        self.table = GPIOConfTable()
        # 设置单元格格式
        self.update_table()

        # 设置右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.menu)

        # 水平布局用于按钮
        button = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_table)
        button.addWidget(clear_button)
        generate_button = QPushButton("Gen")
        generate_button.clicked.connect(self.Gen)
        button.addWidget(generate_button)

        # 创建布局并将表格加入
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button)
        self.setLayout(layout)

    # 清除表格内容
    def clear_table(self):
        self.DEVICES = {"GPIO": ["A"], "UART": [], "SPI": [], "I2C": [], "TIM": [], "WDG": []}  # 设备
        self.update_table()

    # 生成配置
    def Gen(self):
        # 读取表格内容
        self.gpio_config = {}
        for i, gpio in enumerate(self.DEVICES["GPIO"]):
            self.gpio_config[gpio] = []
            for j in range(1, 16):
                port = self.table.item(2, i*16+j).text()
                if port == "":
                    self.gpio_config[gpio].append(port)
                    continue
                device_type, device_num, port_name = self.get_device_type(port)
                port = device_type + device_num + "_" + port_name
                self.gpio_config[gpio].append(port)
        # 退出窗口
        self.accept()

    def get_device_type(self, port):
        device_map = { "RX": "UART", "TX": "UART", "SCK": "SPI", "MOSI": "SPI", 
                       "MISO": "SPI", "CS": "SPI", "SCL": "I2C", "SDA": "I2C"}
        port_name = port[:-1]  # 去掉最后的数字

        if port_name in device_map:
            return device_map[port_name], port[-1], port_name
        elif port_name.endswith("CH"):
            return "TIM", port[1], "CH"+port[-1]

    def update_table(self):
        # 重置表格
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.setColumnCount(len(self.DEVICES["GPIO"])*16+1)

        # 第一行
        self.table.insertRow(self.table.rowCount())
        self.table.set_item(0, 0, "", False, font_size=10)
        for j, gpio in enumerate(self.DEVICES["GPIO"]):
            self.table.setSpan(0, 16*j+1, 1, 16)  # 合并单元格
            self.table.set_item(0, 16*j+1, "GPIO"+gpio, False, font_size=10)
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
        # 如果设备没有配置，则直接返回
        if self.DEVICES[dev] == []:
            return

        # 记录当前设备的行索引
        self.row_indexes[dev] = []

        # 添加新行
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)

        # 创建一个按钮用于折叠/展开
        fold_button = QPushButton(dev)
        fold_button.setCheckable(True)
        fold_button.setChecked(True)  # 设置为默认选中状态
        fold_button.toggled.connect(lambda checked, device=dev: self.fold_row(device, checked))
        self.table.setCellWidget(current_row, 0, fold_button)
        # 其他行合并
        self.table.setSpan(current_row, 1, 1, self.table.columnCount()-1)
        self.table.set_item(current_row, 1, "", False)  # 设置不可编辑的标签
        current_row += 1

        # 插入项目并记录行索引
        for item in self.DEVICES[dev]:
            self.table.insertRow(current_row)
            self.table.set_item(current_row, 0, dev+item, False, font_size=8)
            for j in range(1, self.table.columnCount()):
                self.table.set_item(current_row, j, "", False)  # 设置不可编辑的空白单元格
            self.row_indexes[dev].append(current_row)  # 记录行索引
            current_row += 1

        self.fold_row(dev, True)  # 默认不折叠

    def fold_row(self, dev, checked):
        # 获取当前设备的项目行索引
        if dev not in self.row_indexes:
            return
        if checked:  # 如果按钮被检查（展开）
            # 显示项目行
            for row in self.row_indexes[dev]:
                self.table.setRowHidden(row, False)
        else:  # 如果按钮未被检查（折叠）
            # 隐藏项目行
            for row in self.row_indexes[dev]:
                self.table.setRowHidden(row, True)

    # 右键菜单
    def menu(self, position):
        selected_item = self.table.currentItem()
        try:
            self.row = selected_item.row()
            self.col = selected_item.column()
            if self.row > 0 and self.col == 0:
                type = self.table.item(self.row, 0).text()
                if type == "PIN":
                    self.create_menu(["+ GPIO"], position, "DEVICE")
                else:
                    self.create_menu(["+ UART", "+ SPI", "+ I2C", "+ TIM"], position, "DEVICE")
            else:
                device_name = self.table.item(self.row, 0).text()
                device = device_name[:-1]  # 提取字母
                num = device_name[-1]  # 提取数字
                if device == "UART":
                    if self.chech_row():
                        menu_list = [f"RX{num}", f"TX{num}", ""]
                    else:
                        menu_list = [f"TX{num}", ""]  # 删除 RX
                elif device == "SPI":
                    if self.chech_row():
                        menu_list = [f"SCK{num}", f"MOSI{num}", f"MISO{num}", f"CS{num}", ""]
                    else:
                        menu_list = [f"SCK{num}", f"MOSI{num}", f"CS{num}", ""]  # 删除 MISO
                elif device == "I2C":
                    menu_list = [f"SCL{num}", f"SDA{num}", ""]
                elif device == "TIM":
                    menu_list = [f"T{num}CH1", f"T{num}CH2", f"T{num}CH3", f"T{num}CH4", ""]
                # 根据设备类型创建右键菜单
                if menu_list:
                    self.create_menu(menu_list, position)
        except:
            return

    # 创建右键菜单并连接信号与槽
    def create_menu(self, menu_list, position, mode="PIN"):
        menu = QMenu()
        if mode == "PIN":
            for text in menu_list:
                menu_action = menu.addAction(text)
                menu_action.triggered.connect(lambda checked, content=text: self.fill_cell(content))
            # 在点击的地方显示菜单
        elif mode == "DEVICE":
            for text in menu_list:
                menu_action = menu.addAction(text)
                menu_action.triggered.connect(lambda checked, content=text: self.add_device(content))
        menu.exec_(self.table.viewport().mapToGlobal(position))

    # 检查是否已经使用 RX MISO
    def chech_row(self):
        for j in range(self.table.columnCount() - 1):
            try:
                if ''.join(filter(str.isalpha, self.table.item(self.row, j + 1).text())) in ["RX", "MISO"]:
                    return False
            except:
                pass
        return True

    # 检查列是否有值
    def chech_col(self):
        col_list = []
        for i in range(self.table.rowCount() - 3):
            try:
                if self.table.item(i + 3, self.col).text():  # 检查单元格是否有内容
                    col_list.append((i + 3, self.col))
            except:
                pass
        return col_list

    # 添加设备
    def add_device(self, device_name):
        if device_name == "+ GPIO":
            self.DEVICES["GPIO"].append(f"{chr(ord('A') + len(self.DEVICES['GPIO']))}")
        elif device_name == "+ UART":
            self.DEVICES["UART"].append(f"{len(self.DEVICES['UART'])+1}")
        elif device_name == "+ SPI":
            self.DEVICES["SPI"].append(f"{len(self.DEVICES['SPI'])+1}")
        elif device_name == "+ I2C":
            self.DEVICES["I2C"].append(f"{len(self.DEVICES['I2C'])+1}")
        elif device_name == "+ TIM":
            self.DEVICES["TIM"].append(f"{len(self.DEVICES['TIM'])+1}")
        self.update_table()

    # 填充单元格内容
    def fill_cell(self, content):
        if self.row is None or self.col is None:
            return  # 如果当前行或列为空，直接返回
        if content:
            col_list = self.chech_col()
            self.table.item(self.row, 0).setBackground(QColor('lightgreen'))
            if col_list == []:  # 检查列是否有值
                self.table.set_item(2, self.col, content, False, "lightgreen")
                self.table.set_item(self.row, self.col, content, False, "lightgreen")
            else:
                for item in col_list:
                    self.table.item(item[0], item[1]).setBackground(QColor('red'))
                self.table.set_item(2, self.col, "", False, "red")
                self.table.set_item(self.row, self.col, content, False, "red")
        else:
            self.table.set_item(self.row, self.col, "", False, "white")
            col_list = self.chech_col()
            if col_list:
                if len(col_list) == 1:  # 列只有一个值
                    text = self.table.item(col_list[0][0], col_list[0][1]).text()
                    self.table.set_item(2, self.col, text, False, "lightgreen")
                    self.table.item(col_list[0][0], col_list[0][1]).setBackground(QColor('lightgreen'))
            else:
                self.table.set_item(2, self.col, "", False, "white")
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIOConf()
    window.show()
    sys.exit(app.exec_())



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QMenu, QAction, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt

DEVICES = {
    "UART": ["UART1", "UART2", "UART3"],
    "SPI": ["SPI1", "SPI2"],
    "I2C": ["I2C1", "I2C2"],
    "TIM": ["TIM1", "TIM2", "TIM3", "TIM4"],
    "WDG": ["IWDG", "WWDG"]
}

FILL_OPTIONS = {
    "UART": [f"RX{num}" for num in range(10)] + [f"TX{num}" for num in range(10)] + ["None"],
    "SPI": [f"SCK{num}" for num in range(10)] + [f"MISO{num}" for num in range(10)] + [f"MOSI{num}" for num in range(10)] + [f"CS{num}" for num in range(10)] + ["None"],
    "I2C": [f"SCL{num}" for num in range(10)] + [f"SDA{num}" for num in range(10)] + ["None"],
    "TIM": [f"T{num}CH{i}" for num in range(1, 5) for i in range(1, 5)] + ["None"]
}

class TableExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("设备表格示例")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(self.get_device_count())
        self.table_widget.setColumnCount(17)
        self.table_widget.setHorizontalHeaderLabels(["设备"] + [f"列 {i+1}" for i in range(16)])

        self.populate_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        central_widget.setLayout(layout)

        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.open_context_menu)

    def get_device_count(self):
        return sum(len(devices) for devices in DEVICES.values())

    def populate_table(self):
        row = 0
        for device_type, devices in DEVICES.items():
            for device in devices:
                self.table_widget.setItem(row, 0, QTableWidgetItem(device))
                for col in range(1, 17):
                    self.table_widget.setItem(row, col, QTableWidgetItem(""))  # 初始化为空
                row += 1

    def open_context_menu(self, position):
        menu = QMenu()
        selected_item = self.table_widget.currentItem()

        if selected_item and selected_item.column() > 0:
            row = selected_item.row()
            device_name = self.table_widget.item(row, 0).text()
            device_type = next((dt for dt, devices in DEVICES.items() if device_name in devices), None)

            if device_type and device_type in FILL_OPTIONS:
                options = FILL_OPTIONS[device_type]

                for option in options:
                    action = QAction(option, self)
                    action.triggered.connect(lambda checked, r=row, c=selected_item.column(), o=option: self.fill_cell(r, c, o))
                    menu.addAction(action)

            menu.addSeparator()
            add_device_action = QAction("添加设备", self)
            add_device_action.triggered.connect(self.add_device)
            menu.addAction(add_device_action)

            menu.exec_(self.table_widget.viewport().mapToGlobal(position))

    def fill_cell(self, row, column, option):
        self.table_widget.setItem(row, column, QTableWidgetItem(option))
        self.check_for_errors()  # 每次填入后检查错误

        # 检查是否合法并设置颜色
        if option and option != "None":
            is_valid = self.validate_pin(row, column, option)
            if is_valid:
                self.table_widget.item(row, column).setBackground(QColor("green"))  # 合法时设置为绿色
            else:
                self.table_widget.item(row, column).setBackground(QColor("red"))  # 非法时设置为红色

    def validate_pin(self, row, column, option):
        # 检查该单元格填入的引脚是否合法
        pin_usage = {}

        # 检查每列
        for col in range(1, 17):
            for r in range(self.table_widget.rowCount()):
                item = self.table_widget.item(r, col)
                if item and item.text() != "":
                    pin = item.text()
                    if pin in pin_usage:
                        pin_usage[pin].append(r)
                    else:
                        pin_usage[pin] = [r]

        # 检查行中是否有相同引脚
        for c in range(1, 17):
            used_pins = set()
            for r in range(self.table_widget.rowCount()):
                item = self.table_widget.item(r, c)
                if item and item.text() != "":
                    pin = item.text()
                    if pin in used_pins:
                        return False  # 行中相同引脚
                    used_pins.add(pin)

        return True

    def check_for_errors(self):
        errors = set()  # 用于存储错误单元格

        # 检查每列
        for col in range(1, 17):
            devices = {}
            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, col)
                if item and item.text() != "":
                    pin = item.text()
                    if pin in devices:
                        devices[pin].append(row)
                    else:
                        devices[pin] = [row]

            for pin, rows in devices.items():
                if len(rows) > 1:  # 如果某列有多个设备的引脚
                    errors.update(rows)

        # 更新单元格颜色
        for row in range(self.table_widget.rowCount()):
            for col in range(1, 17):
                item = self.table_widget.item(row, col)
                if item:
                    if row in errors:
                        item.setBackground(QColor("red"))
                    else:
                        item.setBackground(QColor("white"))  # 重置背景颜色

    def add_device(self):
        # 输入设备类型
        device_type, ok = QInputDialog.getItem(self, "选择设备类型", "设备类型:", list(DEVICES.keys()), 0, False)
        if ok and device_type:
            # 输入设备名称
            device_name, ok = QInputDialog.getText(self, "输入设备名称", "设备名称:")
            if ok and device_name:
                if device_name not in DEVICES[device_type]:  # 确保设备名称唯一
                    DEVICES[device_type].append(device_name)
                    self.update_table()  # 更新表格
                else:
                    QMessageBox.warning(self, "警告", "设备名称已存在！")

    def update_table(self):
        self.table_widget.setRowCount(self.get_device_count())  # 更新行数
        self.populate_table()  # 重新填充表格

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TableExample()
    mainWin.show()
    sys.exit(app.exec_())

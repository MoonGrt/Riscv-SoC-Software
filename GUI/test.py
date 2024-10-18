import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QInputDialog, QTableWidgetItem

class CustomTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.current_row = None
        self.current_column = None

    def mousePressEvent(self, event):
        # 判断是否是右键点击
        if event.button() == 2:  # Qt.RightButton
            # 记录当前点击的单元格位置
            item = self.itemAt(event.pos())
            if item:
                self.current_row = item.row()
                self.current_column = item.column()
            else:
                self.current_row, self.current_column = None, None
            self.show_selection_dialog()
        else:
            super().mousePressEvent(event)  # 调用父类处理其他鼠标事件

    def show_selection_dialog(self):
        # 选项列表
        options = ["Option A", "Option B", "Option C"]
        
        # 弹出一个输入对话框，允许用户选择
        option, ok = QInputDialog.getItem(self, "Select an option", "Choose a value to fill in:", options, 0, False)
        
        # 如果用户确认选择并且当前单元格有效，填入选中的内容
        if ok and self.current_row is not None and self.current_column is not None:
            self.setItem(self.current_row, self.current_column, QTableWidgetItem(option))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = CustomTableWidget(3, 3)

    # 添加一些示例数据
    for i in range(3):
        for j in range(3):
            table.setItem(i, j, QTableWidgetItem(f"Item {i+1},{j+1}"))

    table.show()
    sys.exit(app.exec_())

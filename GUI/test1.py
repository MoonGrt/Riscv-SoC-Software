import sys, random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPathItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QPainterPath, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF, QEvent

class Block(QGraphicsRectItem):
    def __init__(self, x, y, name, scene, color):
        super().__init__(-40, -20, 80, 40)  # 块的大小: 80x40
        self.setPos(x, y)
        self.initial_pos = QPointF(x, y)  # 存储初始位置
        self.setBrush(color)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)  # 允许移动
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)  # 允许选择
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges, True)  # 启用几何变化通知
        self.scene = scene
        self.name = name
        self.connections = []  # 存储连接的线
        self.selected = False  # 跟踪块的选择状态

        # 添加标签（居中的文本）
        self.text = self.scene.addText(name)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setParentItem(self)
        self.update_text_position()

    def update_text_position(self):
        """保持文本在块内居中显示。"""
        text_rect = self.text.boundingRect()  # 获取文本的边界矩形
        rect = self.rect()  # 获取块的矩形
        self.text.setPos(-text_rect.width() / 2, -text_rect.height() / 2)  # 设置文本位置，使其居中

    def add_connection(self, curve):
        self.connections.append(curve)  # 添加连接

    def update_connections(self):
        """更新所有连接的曲线。"""
        for curve in self.connections:  # 遍历所有连接
            curve.update_path()  # 更新每个连接的路径

    def itemChange(self, change, value):
        """当块的位置发生变化时，更新连接。"""
        if change == QGraphicsItem.ItemPositionChange:
            self.update_connections()  # 更新连接
        return super().itemChange(change, value)

    def left_center(self):
        """获取块的左中点。"""
        rect = self.rect()
        return self.scenePos() + QPointF(rect.left(), rect.center().y())

    def right_center(self):
        """获取块的右中点。"""
        rect = self.rect()
        return self.scenePos() + QPointF(rect.right(), rect.center().y())

    def reset_position(self):
        """将块重置为初始位置。"""
        self.setPos(self.initial_pos)  # 设置位置为初始位置
        self.update_connections()  # 更新连接

    def toggle_selection(self):
        """切换块的选择状态。"""
        self.selected = not self.selected  # 切换状态
        if self.selected:
            self.setBrush(Qt.green)  # 选中时将块高亮为绿色
        else:
            self.setBrush(Qt.lightGray)  # 未选中时为浅灰色

class Connection(QGraphicsPathItem):
    def __init__(self, start_block, end_block):
        super().__init__()
        self.setPen(QPen(Qt.black, 2))  # 设置连接线颜色和宽度
        self.start_block = start_block
        self.end_block = end_block
        start_block.add_connection(self)  # 在起始块中添加连接
        end_block.add_connection(self)  # 在结束块中添加连接
        self.update_path()  # 更新连接路径

    def update_path(self):
        """使用块的左中点和右中点来绘制连接。"""
        start_pos = self.start_block.right_center()  # 获取起始块的右中点
        end_pos = self.end_block.left_center()  # 获取结束块的左中点
        # 定义贝塞尔曲线的控制点
        ctrl1 = QPointF((start_pos.x() + end_pos.x()) / 2, start_pos.y())
        ctrl2 = QPointF((start_pos.x() + end_pos.x()) / 2, end_pos.y())
        # 创建平滑曲线，使用 QPainterPath
        path = QPainterPath()
        path.moveTo(start_pos)  # 移动到起始位置
        path.cubicTo(ctrl1, ctrl2, end_pos)  # 绘制贝塞尔曲线
        self.setPath(path)  # 设置路径


class FlowChart(QWidget):
    def __init__(self):
        super().__init__()
        # 创建布局
        self.layout = QVBoxLayout(self)

        # 图形视图和场景
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿以实现更平滑的渲染
        self.blocks = []  # 存储所有块
        self.connections = []  # 存储所有连接
        self.right_click_block = None  # 跟踪右键选择的块

        # 在底部添加按钮
        self.button_layout = QHBoxLayout()
        self.reset_button = QPushButton("Reset")
        self.confirm_button = QPushButton("Confirm")
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.confirm_button)
        # 连接按钮信号
        self.reset_button.clicked.connect(self.reset_blocks)  # 连接重置按钮
        self.confirm_button.clicked.connect(self.generate_netlist)  # 连接确认按钮

        # 将图形视图和按钮添加到布局中
        self.layout.addWidget(self.view)
        self.layout.addLayout(self.button_layout)

        # 添加主要块
        self.create_blocks_and_connections()

        # 右键连接的变量
        self.selected_block = None
        self.is_selecting = False
        # 设置右键事件
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.on_right_click)
        # 
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)

    def create_blocks_and_connections(self):
        """创建块和连接，并分配颜色。"""
        # 添加多个块
        block1 = self.add_block(50, 200, "VI", Qt.lightGray)
        block2 = self.add_block(200, 200, "Cutter", Qt.lightGray)
        block3 = self.add_block(350, 200, "Filter", Qt.lightGray)
        block4 = self.add_block(500, 150, "Color", Qt.lightGray)
        block5 = self.add_block(500, 250, "Scaler", Qt.lightGray)
        block6 = self.add_block(650, 100, "Bit", Qt.lightGray)
        block7 = self.add_block(650, 200, "Edge", Qt.lightGray)
        block8 = self.add_block(800, 150, "Filler", Qt.lightGray)
        block9 = self.add_block(950, 150, "VO", Qt.lightGray)
        # 添加连接
        self.add_connection(block1, block2)  # VI -> Cutter
        self.add_connection(block2, block3)  # Cutter -> Filter
        self.add_connection(block3, block4)  # Filter -> Color
        self.add_connection(block3, block5)  # Filter -> Scaler
        self.add_connection(block4, block6)  # Color -> Bit
        self.add_connection(block4, block7)  # Color -> Edge
        self.add_connection(block5, block8)  # Scaler -> Filler
        self.add_connection(block6, block8)  # Bit -> Filler
        self.add_connection(block7, block8)  # Edge -> Filler
        self.add_connection(block8, block9)  # Filler -> VO

    def add_block(self, x, y, name, color):
        """添加一个块到场景中。"""
        block = Block(x, y, name, self.scene, color)  # 创建块实例
        self.scene.addItem(block)  # 将块添加到场景
        self.blocks.append(block)  # 将块添加到块列表
        return block

    def add_connection(self, start_block, end_block):
        """添加连接线。"""
        connection = Connection(start_block, end_block)  # 创建连接实例
        self.scene.addItem(connection)  # 将连接添加到场景
        self.connections.append(connection)  # 将连接添加到连接列表

    def reset_blocks(self):
        """重置所有块到其初始位置。"""
        for block in self.blocks:
            block.reset_position()  # 遍历每个块并重置

    def generate_netlist(self):
        """生成连接的网络列表（netlist）。"""
        netlist = []  # 存储网络列表
        for connection in self.connections:
            netlist.append(f"{connection.start_block.name} -> {connection.end_block.name}")  # 添加连接信息
        print("Netlist:")
        print("\n".join(netlist))  # 打印网络列表

    def on_right_click(self, pos):
        """处理右键点击事件以连接块。"""
        item = self.view.itemAt(pos)  # 获取点击位置的项

        # 如果点击的是方块本身（QGraphicsRectItem），而不是文本
        if isinstance(item, QGraphicsRectItem):
            selected_item = item
        # 如果点击的是文本项（QGraphicsTextItem），获取其父级方块（QGraphicsRectItem）
        elif isinstance(item, QGraphicsTextItem):
            selected_item = item.parentItem()  # 获取父级 QGraphicsRectItem
        else:
            selected_item = None
        # 右键连接的逻辑
        if selected_item and isinstance(selected_item, Block):
            if self.right_click_block:
                if self.right_click_block != selected_item:
                    # 创建连接
                    self.add_connection(self.right_click_block, selected_item)
                # 重置右键选择的块
                self.right_click_block.setBrush(Qt.lightGray)
                self.right_click_block = None
            else:
                self.right_click_block = selected_item  # 记录右键点击的块
                selected_item.toggle_selection()  # 高亮右键点击的块

    def eventFilter(self, source, event):
        """Handle middle mouse button events to delete connections."""
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                pos = event.pos()
                item = self.view.itemAt(pos)
                if isinstance(item, Connection):
                    # If a connection is clicked with the middle button, delete it
                    self.scene.removeItem(item)
                    self.connections.remove(item)
                return True  # Event handled
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlowChart()
    window.setWindowTitle("BlockDesigner")
    window.resize(1100, 600)
    window.show()
    sys.exit(app.exec_())

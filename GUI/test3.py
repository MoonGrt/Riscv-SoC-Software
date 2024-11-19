import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor

class MindMapNode(QGraphicsEllipseItem):
    """思维导图的节点类"""
    def __init__(self, x, y, text, parent=None):
        super().__init__(-50, -25, 100, 50, parent)  # 定义节点为椭圆
        self.setBrush(QBrush(QColor("lightblue")))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsScenePositionChanges)
        
        # 添加文字
        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setDefaultTextColor(Qt.black)
        self.text_item.setPos(-40, -15)  # 调整文字位置

    def itemChange(self, change, value):
        """在节点移动时更新相关连接线"""
        if change == QGraphicsEllipseItem.ItemPositionChange:
            for line in self.scene().lines:
                line.update_position()
        return super().itemChange(change, value)


class ConnectionLine(QGraphicsLineItem):
    """节点之间的连线"""
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.black, 2))

    def update_position(self):
        """动态更新线条位置"""
        start = self.start_item.scenePos()
        end = self.end_item.scenePos()
        self.setLine(start.x(), start.y(), end.x(), end.y())


class MindMapView(QGraphicsView):
    """思维导图的视图"""
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(-500, -500, 1000, 1000)

        # 节点集合
        node1 = MindMapNode(0, 0, "中心主题")
        node2 = MindMapNode(200, 100, "分支1")
        node3 = MindMapNode(200, -100, "分支2")
        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)

        # 连线集合
        self.line1 = ConnectionLine(node1, node2)
        self.line2 = ConnectionLine(node1, node3)
        self.scene.addItem(self.line1)
        self.scene.addItem(self.line2)
        self.scene.lines = [self.line1, self.line2]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MindMapView()
    view.setWindowTitle("思维导图")
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())

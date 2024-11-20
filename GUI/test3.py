import sys
from PyQt5.QtCore import Qt, QRectF, QLineF
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsItem

class FlowchartView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)

class FlowchartScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # Create blocks (rectangles)
        self.blocks = {}
        self.create_block(50, 50, "VI", "input")
        self.create_block(250, 50, "Cutter", "process")
        self.create_block(450, 50, "Filter", "process")
        self.create_block(250, 200, "Bit", "output")
        self.create_block(450, 200, "Color", "output")
        self.create_block(650, 200, "Edge", "output")
        self.create_block(250, 350, "Scaler", "process")
        self.create_block(450, 350, "VO", "output")

        # Create arrows (lines) between blocks
        self.arrows = []
        self.create_arrow(self.blocks["VI"], self.blocks["Cutter"])
        self.create_arrow(self.blocks["Cutter"], self.blocks["Filter"])
        self.create_arrow(self.blocks["Filter"], self.blocks["Bit"])
        self.create_arrow(self.blocks["Filter"], self.blocks["Color"])
        self.create_arrow(self.blocks["Filter"], self.blocks["Edge"])
        self.create_arrow(self.blocks["Bit"], self.blocks["Scaler"])
        self.create_arrow(self.blocks["Color"], self.blocks["Scaler"])
        self.create_arrow(self.blocks["Edge"], self.blocks["Scaler"])
        self.create_arrow(self.blocks["Scaler"], self.blocks["VO"])

    def create_block(self, x, y, text, block_type):
        rect = QGraphicsRectItem(QRectF(x, y, 100, 40))
        rect.setFlag(QGraphicsItem.ItemIsMovable)  # Enable dragging
        if block_type == "input":
            rect.setBrush(QBrush(Qt.green))
        elif block_type == "process":
            rect.setBrush(QBrush(Qt.yellow))
        else:
            rect.setBrush(QBrush(Qt.blue))

        self.addItem(rect)

        label = TextItem(text, rect)
        label.setPos(x + 20, y + 10)
        self.addItem(label)

        # Store block for future reference (keyed by text name)
        self.blocks[text] = rect

    def create_arrow(self, start_block, end_block):
        line = ArrowLine(start_block, end_block)
        self.addItem(line)
        self.arrows.append(line)

class ArrowLine(QGraphicsLineItem):
    def __init__(self, start_block, end_block):
        super().__init__()
        self.start_block = start_block
        self.end_block = end_block
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.update_line()

    def update_line(self):
        start_center = self.start_block.sceneBoundingRect().center()
        end_center = self.end_block.sceneBoundingRect().center()
        self.setLine(QLineF(start_center, end_center))

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.update_line()  # Update the line when the position of the blocks changes
        return super().itemChange(change, value)

class TextItem(QGraphicsTextItem):
    def __init__(self, text, parent_block):
        super().__init__(text, parent_block)
        self.parent_block = parent_block  # The block this text item is associated with

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            new_pos = self.parent_block.scenePos() + value
            self.setPos(new_pos.x() + 20, new_pos.y() + 10)  # Adjust position relative to the block
        return super().itemChange(change, value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = FlowchartScene()
    view = FlowchartView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setScene(scene)
    view.setGeometry(100, 100, 800, 600)
    view.show()
    sys.exit(app.exec_())

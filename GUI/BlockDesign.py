import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QVBoxLayout, QHBoxLayout, QListWidget, QWidget, QLabel, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPointF


class BlockItem(QGraphicsRectItem):
    """Custom block item to represent a module with ports."""
    def __init__(self, name, x, y, width=100, height=50):
        super().__init__(x, y, width, height)
        self.setBrush(QBrush(Qt.lightGray))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.name = name

        # Add input and output ports
        self.input_port = QGraphicsEllipseItem(-10, height / 2 - 5, 10, 10, self)
        self.input_port.setBrush(QBrush(Qt.blue))
        self.output_port = QGraphicsEllipseItem(width, height / 2 - 5, 10, 10, self)
        self.output_port.setBrush(QBrush(Qt.green))


class ConnectionLine(QGraphicsLineItem):
    """Custom connection line between ports."""
    def __init__(self, start_port, end_port=None):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.setPen(QPen(Qt.black, 2))
        self.update_line()

    def update_line(self):
        """Update the line's start and end points."""
        start_pos = self.start_port.scenePos() + QPointF(5, 5)
        if self.end_port:
            end_pos = self.end_port.scenePos() + QPointF(5, 5)
        else:
            end_pos = start_pos  # Temporary line
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())


class BlockDesignApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block Design GUI")
        self.resize(1200, 800)
        
        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout()
        main_widget.setLayout(layout)
        
        # Left Panel (Module List)
        self.module_list = QListWidget()
        self.module_list.addItems(["Adder", "Multiplier", "FIFO", "AXI Interconnect"])
        self.module_list.itemDoubleClicked.connect(self.add_block)
        layout.addWidget(self.module_list, 1)
        
        # Center (Design Area)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing
        layout.addWidget(self.view, 4)
        
        # Right Panel (Properties)
        self.properties_panel = QWidget()
        self.properties_layout = QFormLayout()
        self.properties_panel.setLayout(self.properties_layout)
        layout.addWidget(self.properties_panel, 2)
        
        self.selected_block_label = QLabel("No block selected")
        self.properties_layout.addRow("Selected Block:", self.selected_block_label)
        self.block_name_edit = QLineEdit()
        self.block_name_edit.setEnabled(False)
        self.properties_layout.addRow("Block Name:", self.block_name_edit)
        
        # Signal Connections
        self.scene.selectionChanged.connect(self.update_properties)

        # Connection state
        self.current_line = None
        self.connections = []  # Store connections (start_port, end_port)
        
    def add_block(self, item):
        """Add a new block to the design area."""
        name = item.text()
        block = BlockItem(name, 0, 0)
        self.scene.addItem(block)
        block.input_port.mousePressEvent = lambda event: self.start_connection(block.input_port, event)
        block.output_port.mousePressEvent = lambda event: self.start_connection(block.output_port, event)
    
    def start_connection(self, port, event):
        """Start a connection from a port."""
        if self.current_line is None:  # Start a new connection
            self.current_line = ConnectionLine(port)
            self.scene.addItem(self.current_line)
        else:  # Complete the connection
            self.current_line.end_port = port
            self.current_line.update_line()
            self.connections.append((self.current_line.start_port, self.current_line.end_port))
            self.current_line = None

    def mouseMoveEvent(self, event):
        """Update the temporary connection line during mouse drag."""
        if self.current_line:
            cursor_pos = self.view.mapToScene(event.pos())
            self.current_line.setLine(
                self.current_line.start_port.scenePos().x() + 5,
                self.current_line.start_port.scenePos().y() + 5,
                cursor_pos.x(), cursor_pos.y()
            )

    def update_properties(self):
        """Update the properties panel based on the selected block."""
        selected_items = self.scene.selectedItems()
        if selected_items:
            block = selected_items[0]
            if isinstance(block, BlockItem):
                self.selected_block_label.setText(block.name)
                self.block_name_edit.setText(block.name)
                self.block_name_edit.setEnabled(True)
                self.block_name_edit.textChanged.connect(lambda text: setattr(block, 'name', text))
        else:
            self.selected_block_label.setText("No block selected")
            self.block_name_edit.clear()
            self.block_name_edit.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlockDesignApp()
    window.show()
    sys.exit(app.exec())

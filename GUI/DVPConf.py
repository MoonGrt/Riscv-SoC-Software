import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPathItem, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDialog, QListWidget, QFormLayout, QLabel, QLineEdit
from PyQt5.QtGui import QPen, QPainterPath, QPainter, QColor, QIcon
from PyQt5.QtCore import Qt, QPointF, QEvent

class Block(QGraphicsRectItem):
    def __init__(self, x, y, block_type, name, scene, color):
        super().__init__(-30, -15, 60, 30)  # 块的大小: 60x30
        self.setPos(x, y)
        self.initial_pos = QPointF(x, y)  # 存储初始位置
        self.setBrush(color)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)  # 允许移动
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)  # 允许选择
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges, True)  # 启用几何变化通知
        self.scene = scene
        self.block_type = block_type
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
        self.text.setPos(-text_rect.width() / 2, -text_rect.height() / 2)  # 设置文本位置，使其居中

    def update_name(self, name):
        """更新块的名称。"""
        self.name = name
        self.text.setPlainText(name)  # 更新文本内容
        self.update_text_position()  # 保持文本居中显示
        self.scene.update()  # 刷新视图

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


class Connection(QGraphicsPathItem):
    def __init__(self, start_block: Block, end_block: Block):
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


class BlockDesigner(QGraphicsView):
    def __init__(self, Block_label: QLabel, Name_label: QLineEdit):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿以实现更平滑的渲染

        self.Block_label = Block_label
        self.Name_label = Name_label
        self.blocks = []  # 存储所有块
        self.connections = []  # 存储所有连接
        self.left_click_block = None  # 左键选择的块
        self.right_click_block = None  # 右键选择的块

        # 添加主要块
        self.create_blocks_and_connections()
        self.add_splitter()  # 添加分割线

    def create_blocks_and_connections(self):
        """创建块和连接，并分配颜色。"""
        block_test = self.add_block(20, 100, "Test", "Test", QColor("#6495ED"))
        block_hdmi_in = self.add_block(20, 200, "HDMI_RX", "HDMI", QColor("#6495ED"))  # 指向 VI 的 HDMI
        block_cam = self.add_block(20, 300, "CAM", "CAM", QColor("#6495ED"))
        block2 = self.add_block(160, 200, "Cutter", "Cutter", QColor("#8CBAB7"))
        block3 = self.add_block(260, 200, "Filter", "Filter", QColor("#8CBAB7"))
        block4 = self.add_block(360, 150, "Color", "Color", QColor("#8CBAB7"))
        block5 = self.add_block(440, 300, "Scaler", "Scaler", QColor("#8CBAB7"))
        block6 = self.add_block(460, 100, "Bit", "Bit", QColor("#8CBAB7"))
        block7 = self.add_block(460, 200, "Edger", "Edger", QColor("#8CBAB7"))
        block8 = self.add_block(560, 150, "Filler", "Filler", QColor("#8CBAB7"))
        block_hdmi_out = self.add_block(700, 50, "HDMI_TX", "HDMI", QColor("#6495ED"))  # VO 指向的 HDMI
        block_lcd = self.add_block(700, 150, "LCD", "LCD", QColor("#6495ED"))
        block_vga = self.add_block(700, 250, "VGA", "VGA", QColor("#6495ED"))

        self.add_connection(block_test, block2)     # Test -> Cutter
        self.add_connection(block_hdmi_in, block2)  # HDMI_IN -> Cutter
        self.add_connection(block_cam, block2)     # CAM -> Cutter
        self.add_connection(block2, block3)  # Cutter -> Filter
        self.add_connection(block3, block4)  # Filter -> Color
        self.add_connection(block3, block5)  # Filter -> Scaler
        self.add_connection(block4, block6)  # Color -> Bit
        self.add_connection(block4, block7)  # Color -> Edger
        self.add_connection(block5, block8)  # Scaler -> Filler
        self.add_connection(block6, block8)  # Bit -> Filler
        self.add_connection(block7, block8)  # Edger -> Filler
        self.add_connection(block8, block_hdmi_out)  # Filler -> HDMI_OUT
        self.add_connection(block8, block_lcd)     # Filler -> LCD
        self.add_connection(block8, block_vga)     # Filler -> VGA

    def add_block(self, x, y, block_type, name, color):
        """添加一个块到场景中。"""
        for block in self.blocks:
            if block.block_type == block_type and block.name == name:
                print(f"Block {block_type} {name} already exists.")
                return None  # 块已存在，返回 None
        block = Block(x, y, block_type, name, self.scene, color)  # 创建块实例
        self.scene.addItem(block)  # 将块添加到场景
        self.blocks.append(block)  # 将块添加到块列表
        return block

    def add_connection(self, start_block, end_block):
        """添加连接线。"""
        for connection in self.connections:
            if connection.start_block == start_block and connection.end_block == end_block:
                print(f"Connection between {start_block.name} and {end_block.name} already exists.")
                return  # 连接已存在，返回
        connection = Connection(start_block, end_block)  # 创建连接实例
        self.scene.addItem(connection)  # 将连接添加到场景
        self.connections.append(connection)  # 将连接添加到连接列表

    def add_splitter(self):
        """添加分割线。"""
        # 设置虚线样式的笔
        dashed_pen = QPen(Qt.black)
        dashed_pen.setStyle(Qt.DashLine)  # 设置为虚线
        dashed_pen.setWidth(1)  # 设置线宽
        self.scene.addLine(120, 0, 120, 400, dashed_pen)  # 添加水平分割线
        self.scene.addLine(600, 0, 600, 400, dashed_pen)  # 添加水平分割线
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_item = self.itemAt(event.pos())  # 获取点击位置的项
            # 如果点击的是方块本身（QGraphicsRectItem），而不是文本
            if isinstance(clicked_item, QGraphicsRectItem):
                selected_item = clicked_item
            # 如果点击的是文本项（QGraphicsTextItem），获取其父级方块（QGraphicsRectItem）
            elif isinstance(clicked_item, QGraphicsTextItem):
                selected_item = clicked_item.parentItem()  # 获取父级 QGraphicsRectItem
            else:
                selected_item = None
            if selected_item and isinstance(selected_item, Block):
                if self.left_click_block:
                    if self.left_click_block != selected_item:
                        try:
                            self.Name_label.textChanged.disconnect()  # 断开文本框信号连接
                        except:
                            pass
                        self.Name_label.textChanged.connect(lambda: selected_item.update_name(self.Name_label.text()))
                else:
                    self.Name_label.textChanged.connect(lambda: selected_item.update_name(self.Name_label.text()))
                self.Block_label.setText(selected_item.block_type)
                self.Name_label.setText(selected_item.name)
                self.Name_label.setEnabled(True)
                self.left_click_block = selected_item  # 记录左键点击的块
            else:
                try:
                    self.Name_label.textChanged.disconnect()  # 断开文本框信号连接
                except:
                    pass
                self.Block_label.setText("----------")
                self.Name_label.setText("")
                self.Name_label.setEnabled(False)
            super().mousePressEvent(event)  # 调用父类方法以更新鼠标位置
        elif event.button() == Qt.RightButton:
            clicked_item = self.itemAt(event.pos())  # 获取点击位置的项
            # 如果点击的是方块本身（QGraphicsRectItem），而不是文本
            if isinstance(clicked_item, QGraphicsRectItem):
                selected_item = clicked_item
            # 如果点击的是文本项（QGraphicsTextItem），获取其父级方块（QGraphicsRectItem）
            elif isinstance(clicked_item, QGraphicsTextItem):
                selected_item = clicked_item.parentItem()  # 获取父级 QGraphicsRectItem
            else:
                selected_item = None
            # 右键连接的逻辑
            if selected_item and isinstance(selected_item, Block):
                try:
                    self.Name_label.textChanged.disconnect()  # 断开文本框信号连接
                except:
                    pass
                self.Block_label.setText(selected_item.block_type)
                self.Name_label.setText(selected_item.name)
                if self.right_click_block:
                    if self.right_click_block != selected_item:
                        # 创建连接
                        self.add_connection(self.right_click_block, selected_item)
                    # 重置右键选择的块
                    if self.right_click_block.name in ["Test", "HDMI", "CAM"]:
                        self.right_click_block.setBrush(QColor("#6495ED"))
                    else:
                        self.right_click_block.setBrush(QColor("#8CBAB7"))
                    self.right_click_block = None
                else:
                    self.right_click_block = selected_item  # 记录右键点击的块
                    self.right_click_block.setBrush(Qt.green)
            else:
                try:
                    self.Name_label.textChanged.disconnect()  # 断开文本框信号连接
                except:
                    pass
                self.Block_label.setText("----------")
                self.Name_label.setText("")
                self.Name_label.setEnabled(False)
        elif event.button() == Qt.MiddleButton:
            clicked_item = self.itemAt(event.pos())  # 获取点击位置的项
            # 如果用中间按钮点击连接，则删除它
            if isinstance(clicked_item, Connection):
                self.scene.removeItem(clicked_item)
                self.connections.remove(clicked_item)
            # 如果用中间按钮点击块，则删除它
            if isinstance(clicked_item, QGraphicsRectItem):
                self.scene.removeItem(clicked_item)
            elif isinstance(clicked_item, QGraphicsTextItem):
                selected_item = clicked_item.parentItem()  # 获取父级 QGraphicsRectItem
                # 删除块及其所有连接
                for connection in selected_item.connections[:]:  # 使用切片复制列表
                    self.scene.removeItem(connection)  # 从场景中移除连接
                    self.connections.remove(connection)  # 从连接列表中移除连接
                    connection.start_block.connections.remove(connection)  # 从起始块的连接中移除
                    connection.end_block.connections.remove(connection)  # 从结束块的连接中移除
                self.scene.removeItem(selected_item)
        else:
            super().mousePressEvent(event)  # 调用父类方法以更新鼠标位置


class DVPConf(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.DVPFunc = {'VI.VI': {'in': [], 'out': ['Cutter.Cutter']}, 'Cutter.Cutter': {'in': ['VI.VI'], 'out': ['Filter.Filter']}, 
                        'Filter.Filter': {'in': ['Cutter.Cutter'], 'out': ['Color.Color', 'Scaler.Scaler']}, 'Color.Color': {'in': ['Filter.Filter'], 'out': ['Bit.Bit', 'Edger.Edger']}, 
                        'Scaler.Scaler': {'in': ['Filter.Filter'], 'out': ['Filler.Filler']}, 'Bit.Bit': {'in': ['Color.Color'], 'out': ['Filler.Filler']}, 
                        'Edger.Edger': {'in': ['Color.Color'], 'out': ['Filler.Filler']}, 'Filler.Filler': {'in': ['Scaler.Scaler', 'Bit.Bit', 'Edger.Edger'], 'out': ['VO.VO']}, 
                        'VO.VO': {'in': ['Filler.Filler'], 'out': []}}  # 定义一个空的函数变量，用于保存DVP功能模块

    def init_ui(self):
        """初始化界面。"""
        # 设置应用图标
        self.setWindowIcon(QIcon("icons/DVP.svg"))
        self.setWindowTitle("DVPConf")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #D1A7A4;")  # 将这里的颜色设置为你想要的颜色

        # 创建属性面板
        self.properties_panel = QWidget()
        self.properties_layout = QFormLayout()
        self.properties_panel.setLayout(self.properties_layout)
        self.block_label = QLabel("----------")
        self.properties_layout.addRow("Block:", self.block_label)
        self.block_name_label = QLineEdit()
        self.block_name_label.setFixedWidth(80)
        self.block_name_label.setEnabled(False)
        self.properties_layout.addRow("Name:", self.block_name_label)

        # 创建模块列表
        self.module_vi_list = QListWidget()
        self.module_vi_list.addItems(["Test", "HDMI", "CAM"])
        self.module_vi_list.doubleClicked.connect(self.add_vi_block)  # 连接双击事件

        self.module_vp_list = QListWidget()
        self.module_vp_list.addItems(["Cutter", "Filter", "Color", "Scaler", "Bit", "Edger", "Filler"])
        self.module_vp_list.doubleClicked.connect(self.add_vp_block)  # 连接双击事件

        self.module_vo_list = QListWidget()
        self.module_vo_list.addItems(["HDMI", "LCD", "VGA"])
        self.module_vo_list.doubleClicked.connect(self.add_vo_block)  # 连接双击事件

        # 创建图形视图和场景
        self.view = BlockDesigner(self.block_label, self.block_name_label)  # 使用自定义的 BlockDesigner

        # 在底部添加按钮
        self.button_layout = QHBoxLayout()
        self.reset_button = QPushButton("Reset")
        self.confirm_button = QPushButton("Confirm")
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.confirm_button)
        # 连接按钮信号
        self.reset_button.clicked.connect(self.reset)  # 连接重置按钮
        self.confirm_button.clicked.connect(self.confirm)  # 连接确认按钮

        # 创建上下布局
        self.Vl_layout = QVBoxLayout()
        self.Vl_layout.addWidget(self.properties_panel)
        self.Vl_layout.addWidget(self.module_vi_list)
        self.Vl_layout.addWidget(self.module_vp_list)
        self.Vl_layout.addWidget(self.module_vo_list)
        # 创建上下布局
        self.Vr_layout = QVBoxLayout()
        self.Vr_layout.addWidget(self.view)
        self.Vr_layout.addLayout(self.button_layout)
        # 创建左右布局
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addLayout(self.Vl_layout, stretch=1)
        self.Hlayout.addLayout(self.Vr_layout, stretch=5)
        # 创建布局
        self.setLayout(self.Hlayout)

    def reset(self):
        """重置所有块到其初始位置。"""
        # for block in self.view.blocks:
        #     block.reset_position()  # 遍历每个块并重置
        self.view.scene.clear()  # 清除场景
        self.view.blocks = []  # 存储所有块
        self.view.connections = []  # 存储所有连接
        self.view.right_click_block = None  # 右键选择的块
        self.view.create_blocks_and_connections()  # 重新创建所有块和连接
        self.view.add_splitter()

    def confirm(self):
        """生成连接的网络列表（netlist）。"""
        self.DVPFunc = {}  # 清空网络列表
        for connection in self.view.connections:
            # dict_temp = {}
            # dict_temp["from"] = [connection.start_block.block_type, connection.start_block.name]
            # dict_temp["to"] = [connection.end_block.block_type, connection.end_block.name]
            # self.DVPFunc.append(dict_temp)  # 存储网络列表
            # self.DVPFunc.append(f"{connection.start_block.block_type}.{connection.start_block.name} -> {connection.end_block.block_type}.{connection.end_block.name}")  # 添加连接信息
            # self.DVPFunc.append([f"{connection.start_block.block_type}.{connection.start_block.name}", f"{connection.end_block.block_type}.{connection.end_block.name}"])  # 添加连接信息
            
            source, target = f"{connection.start_block.block_type}.{connection.start_block.name}", f"{connection.end_block.block_type}.{connection.end_block.name}"
            # 初始化源模块和目标模块的字典
            if source not in self.DVPFunc:
                self.DVPFunc[source] = {"in": [], "out": []}
            if target not in self.DVPFunc:
                self.DVPFunc[target] = {"in": [], "out": []}
            # 更新源模块的输出连接
            self.DVPFunc[source]["out"].append(target)
            # 更新目标模块的输入连接
            self.DVPFunc[target]["in"].append(source)
        print(self.DVPFunc)
        # 退出窗口
        self.accept()

    def add_vi_block(self):
        """根据模块列表中选中的模块，添加一个块到场景中。"""
        selected_module = self.module_vi_list.currentItem().text()  # 获取选中的模块名称
        module_cnt = 0  # 记录模块数量
        for block in self.view.blocks:
            if block.block_type == selected_module:
                module_cnt += 1
        self.view.add_block(320, 50, selected_module, selected_module + str(module_cnt), Qt.lightGray)  # 创建新块并添加到场景中

    def add_vp_block(self):
        """根据模块列表中选中的模块，添加一个块到场景中。"""
        selected_module = self.module_vp_list.currentItem().text()  # 获取选中的模块名称
        module_cnt = 0  # 记录模块数量
        for block in self.view.blocks:
            if block.block_type == selected_module:
                module_cnt += 1
        self.view.add_block(320, 50, selected_module, selected_module + str(module_cnt), Qt.lightGray)  # 创建新块并添加到场景中

    def add_vo_block(self):
        """根据模块列表中选中的模块，添加一个块到场景中。"""
        selected_module = self.module_vo_list.currentItem().text()  # 获取选中的模块名称
        module_cnt = 0  # 记录模块数量
        for block in self.view.blocks:
            if block.block_type == selected_module:
                module_cnt += 1
        self.view.add_block(320, 50, selected_module, selected_module + str(module_cnt), Qt.lightGray)  # 创建新块并添加到场景中


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DVPConf()
    window.show()
    sys.exit(app.exec_())

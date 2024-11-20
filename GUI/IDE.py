import sys, serial, serial.tools.list_ports, os, subprocess, shutil, signal, pexpect
from PyQt5.QtWidgets import QVBoxLayout, QSplitter, QGridLayout, QTableWidget, QLabel, QTableWidgetItem, QHBoxLayout, QMessageBox, QFormLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QTabWidget, QWidget, QPushButton, QTabBar, QComboBox
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QDialog
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QTransform, QColor
from NewPro import NewPro
from RISCVSim.pyriscv import Sim

class Serial(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置主窗口属性
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle('Serial')
        self.setStyleSheet("background-color: #D1B0B0;")
        self.setWindowIcon(QIcon('icons/serial.svg'))

        # 表单布局
        layout = QFormLayout()

        # COM端口选择
        self.com_line_edit = QComboBox()
        self.com_line_edit.addItems([])
        layout.addRow('COM Port:', self.com_line_edit)
        self.com_line_edit.setStyleSheet("background-color: #C0B3B1;")

        # 波特率选择
        self.baud_combo_box = QComboBox()
        self.baud_combo_box.addItems(['4800', '9600', '19200', '115200', '230400'])  # Add your desired baud rates
        self.baud_combo_box.setCurrentText('115200')  # Default value
        layout.addRow('Baud Rate:', self.baud_combo_box)
        self.baud_combo_box.setStyleSheet("background-color: #C0B3B1;")

        # 数据位选择
        self.data_bits_combo_box = QComboBox()
        self.data_bits_combo_box.addItems(['5', '6', '7', '8', '9', '10'])  # Add your desired data bits
        self.data_bits_combo_box.setCurrentText('8')  # Default value
        layout.addRow('Data Bits:', self.data_bits_combo_box)
        self.data_bits_combo_box.setStyleSheet("background-color: #C0B3B1;")

        # 校验位选择
        self.parity_combo_box = QComboBox()
        self.parity_combo_box.addItems(['None', 'Odd', 'Even', 'Mark'])  # Add your desired parity options
        self.parity_combo_box.setCurrentText('None')  # Default value
        layout.addRow('Parity:', self.parity_combo_box)
        self.parity_combo_box.setStyleSheet("background-color: #C0B3B1;")

        # 停止位选择
        self.stop_bit_combo_box = QComboBox()
        self.stop_bit_combo_box.addItems(['1', '1.5', '2'])  # Add your desired stop bits
        self.stop_bit_combo_box.setCurrentText('1')  # Default value
        layout.addRow('Stop Bit:', self.stop_bit_combo_box)
        self.stop_bit_combo_box.setStyleSheet("background-color: #C0B3B1;")

        # 确定按钮
        ok_button = QPushButton('确定')
        ok_button.setStyleSheet("background-color: #C0B3B1;")
        ok_button.clicked.connect(self.accept)

        # 刷新按钮
        refresh_button = QPushButton('刷新')
        refresh_button.setStyleSheet("background-color: #C0B3B1;")
        refresh_button.clicked.connect(self.refresh_ports)
        self.refresh_ports()

        layout.addRow(refresh_button, ok_button)
        self.setLayout(layout)

    def get_config(self):
        # 获取串口设置
        return {
            'port': self.com_line_edit.currentText(),
            'baud_rate': int(self.baud_combo_box.currentText()),
            'data_bits': int(self.data_bits_combo_box.currentText()),
            'parity': self.parity_combo_box.currentText(),
            'stop_bit': float(self.stop_bit_combo_box.currentText())
        }

    def refresh_ports(self):
        # 清除 com_line_edit 下拉框中的现有项
        self.com_line_edit.clear()
        # 使用 pyserial 的 list_ports 获取可用的 COM 端口列表
        ports = [port.device for port in serial.tools.list_ports.comports()]
        # 将端口添加到下拉框中
        self.com_line_edit.addItems(ports)

class GdbThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.gdb_process = None

    def load_prog(self, program):
        self.program = program

    def run(self):
        """ 在子线程中执行 GDB 操作 """
        try:
            # 启动 gdb 进程
            self.gdb_process = pexpect.spawn('/opt/riscv/bin/riscv64-unknown-elf-gdb')
            self._capture_output()  # 捕获并显示输出
            # 输入文件路径
            self.gdb_process.sendline(f'file {self.program}')
            self._capture_output()
            # 连接远程目标
            self.gdb_process.sendline('target extended-remote :3333')
            self._capture_output()
            # 执行监控命令
            self.gdb_process.sendline('monitor reset halt')
            self._capture_output()
            # 加载程序
            self.gdb_process.sendline('load')
            self._capture_output()
            # 继续执行
            self.gdb_process.sendline('continue')
            self._capture_output()
        except Exception as e:
            # self.progress_signal.emit(f'Failed to download: {str(e)}')
            self.gdb_process.terminate()

    def stop_run(self):
        """ 在子线程中执行 GDB 操作 """
        try:
            self.gdb_process.sendline('\x03')  # 发送 ctrl+c
            self.gdb_process.sendline('\x03')  # 发送 ctrl+c
            self.gdb_process.sendline('n')  # 发送 ctrl+c
            self._capture_output()
            self.gdb_process.sendline('quit')
            self._capture_output()
            self.gdb_process.sendline('y')
            self._capture_output()
        except Exception as e:
            self.progress_signal.emit(f'烧录失败: {str(e)}')
            self.gdb_process.terminate()

    def _capture_output(self):
        """ 捕获 GDB 的输出并发送到 UI """
        try:
            # 捕获 GDB 输出直到遇到 '(gdb)' 提示符
            while True:
                index = self.gdb_process.expect(['\n', '(gdb)'], timeout=10)
                if index == 0:  # 如果捕获到新的一行输出
                    output = self.gdb_process.before.decode('utf-8').strip()
                    if output:
                        self.progress_signal.emit(output)  # 更新 UI
                if index == 1:  # 如果遇到 gdb 提示符
                    break
        except pexpect.TIMEOUT:
            self.progress_signal.emit("GDB 超时，未能获取输出")

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Serial = Serial()
        self.Sim = Sim()
        self.init_ui()

        # self.project_name = ''
        # self.project_path = ''
        self.openocd_process = None  # 用于保存 openocd 进程
        self.connect()

    def init_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon('icons/app.svg'))

        # 设置主窗口属性
        self.setGeometry(200, 200, 1600, 900)
        self.setWindowTitle('IDE')
        self.setStyleSheet("background-color: #A68F8B")  # 设置为指定的背景色
        self.showMaximized()

        # 创建菜单栏
        self.menu()

        # 创建文件目录
        self.project_path = "../Workspace"
        self.project_name = self.project_path.split('/')[-1]
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Set the root path to be empty
        self.fileTree = QTreeView(self)
        self.fileTree.setModel(self.model)
        self.fileTree.setRootIndex(self.model.index(os.path.expanduser(self.project_path)))  # Set initial folder to home
        self.fileTree.setHeaderHidden(True)
        self.fileTree.setColumnHidden(1, True)  # Hide the size column
        self.fileTree.setColumnHidden(2, True)  # Hide the type column
        self.fileTree.setColumnHidden(3, True)  # Hide the date modified column
        self.fileTree.doubleClicked.connect(self.loadFileDir)

        # 创建主窗格
        content_pane = QTabWidget()
        file_tab = QWidget()
        simulation_tab = QWidget()
        debug_tab = QWidget()
        content_pane.addTab(file_tab, "File")
        content_pane.addTab(simulation_tab, "Simulation")
        content_pane.addTab(debug_tab, "Debug")


        # 创建左侧的编辑区域
        self.edit_area = QTabWidget(file_tab)  # 用于文件编辑的区域
        self.edit_area.setStyleSheet("background-color: #D1A7A4")  # 设置为指定的背景色
        self.newFile(start_page=True)

        # 汇编代码区域
        assemble_layout = QVBoxLayout()  # 为汇编代码创建垂直布局
        # assemble_label = QLabel("             Assemble Code")
        # assemble_layout.addWidget(assemble_label)  # 添加标签
        self.assemble_code_area = QTextEdit()
        self.assemble_code_area.setStyleSheet("background-color: #CEA69B")  # 设置为指定的背景色
        self.assemble_code_area.setReadOnly(True)
        self.assemble_code_area.setLineWrapMode(QTextEdit.NoWrap) # 设置不自动换行
        assemble_layout.addWidget(self.assemble_code_area)  # 添加文本编辑区域
        # 机械码区域
        machine_layout = QVBoxLayout()  # 为机械码创建垂直布局
        # machine_label = QLabel("             Machine Code")
        # machine_layout.addWidget(machine_label)  # 添加标签
        self.machine_code_area = QTextEdit()
        self.machine_code_area.setStyleSheet("background-color: #CEA69B")  # 设置为指定的背景色
        self.machine_code_area.setReadOnly(True)
        machine_layout.addWidget(self.machine_code_area)  # 添加文本编辑区域
        self.fillfile()

        # 创建水平布局
        file_tab_layout = QHBoxLayout(file_tab)
        file_tab_layout.addWidget(self.edit_area, stretch=6)  # 添加编辑区域
        file_tab_layout.addLayout(assemble_layout, stretch=3)
        file_tab_layout.addLayout(machine_layout, stretch=1)


        # 在 simulation_tab 中创建一个 QGridLayout
        simulation_layout = QGridLayout(simulation_tab)
        # 创建四个表格 设置每个表格的行列数
        self.simulation_code_table = QTableWidget(32, 3)
        self.simulation_label_table = QTableWidget(8, 2)
        self.simulation_data_table = QTableWidget(1024, 9)
        self.simulation_register_table = QTableWidget(32, 2)
        # 创建标签
        text_label = QLabel(" Text")
        label_label = QLabel(" Label")
        data_label = QLabel(" Data")
        register_label = QLabel(" Register")
        # 将小部件添加到 simulation_layout 中
        simulation_layout.addWidget(text_label, 0, 0)
        simulation_layout.addWidget(self.simulation_code_table, 1, 0)
        simulation_layout.addWidget(label_label, 0, 1)
        simulation_layout.addWidget(self.simulation_label_table, 1, 1)
        simulation_layout.addWidget(data_label, 2, 0)
        simulation_layout.addWidget(self.simulation_data_table, 3, 0)
        simulation_layout.addWidget(register_label, 2, 1)
        simulation_layout.addWidget(self.simulation_register_table, 3, 1)
        # 设置 simulation_layout 中四个区域的大小比例
        simulation_layout.setRowStretch(0, 1)    # 设置第一行的伸展因子
        simulation_layout.setRowStretch(1, 15)   # 设置第二行的伸展因子
        simulation_layout.setRowStretch(2, 1)    # 设置第三行的伸展因子
        simulation_layout.setRowStretch(3, 15)   # 设置第四行的伸展因子
        simulation_layout.setColumnStretch(0, 3) # 设置第一列的伸展因子
        simulation_layout.setColumnStretch(1, 1) # 设置第二列的伸展因子

        # 在 debug_tab 中创建一个 QGridLayout
        debug_layout = QGridLayout(debug_tab)
        # 创建四个表格 设置每个表格的行列数
        self.debug_code_table = QTableWidget(32, 3)
        self.debug_label_table = QTableWidget(8, 2)
        self.debug_data_table = QTableWidget(1024, 9)
        self.debug_register_table = QTableWidget(32, 2)
        # 创建标签
        text_label = QLabel(" Text")
        label_label = QLabel(" Label")
        data_label = QLabel(" Data")
        register_label = QLabel(" Register")
        # 将小部件添加到 debug_layout 中
        debug_layout.addWidget(text_label, 0, 0)
        debug_layout.addWidget(self.debug_code_table, 1, 0)
        debug_layout.addWidget(label_label, 0, 1)
        debug_layout.addWidget(self.debug_label_table, 1, 1)
        debug_layout.addWidget(data_label, 2, 0)
        debug_layout.addWidget(self.debug_data_table, 3, 0)
        debug_layout.addWidget(register_label, 2, 1)
        debug_layout.addWidget(self.debug_register_table, 3, 1)
        # 设置 debug_layout 中四个区域的大小比例
        debug_layout.setRowStretch(0, 1)    # 设置第一行的伸展因子
        debug_layout.setRowStretch(1, 15)   # 设置第二行的伸展因子
        debug_layout.setRowStretch(2, 1)    # 设置第三行的伸展因子
        debug_layout.setRowStretch(3, 15)   # 设置第四行的伸展因子
        debug_layout.setColumnStretch(0, 3) # 设置第一列的伸展因子
        debug_layout.setColumnStretch(1, 1) # 设置第二列的伸展因子

        # 表格初始化
        self.table_init()
        # 填充代码到表格中
        self.fillfile()
        self.fillCode()
        self.fillLabel()
        # 设置奇数行背景颜色为天蓝色，偶数行背景颜色为钢蓝色
        for tabel in [self.simulation_code_table, self.simulation_label_table, self.simulation_data_table, self.simulation_register_table]:
            for row in range(self.simulation_code_table.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)
        for tabel in [self.debug_code_table, self.debug_label_table, self.debug_data_table, self.debug_register_table]:
            for row in range(tabel.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)

        # 创建消息窗格
        messages_pane = QTabWidget()
        self.message_tab = QTextEdit()
        self.serial_tab = QTextEdit()
        messages_pane.addTab(self.message_tab, "Message  ")
        messages_pane.addTab(self.serial_tab, "Serial  ")

        # Message窗口添加按钮
        message_clear_bottom = QPushButton(QIcon(QIcon("icons/clear.svg").pixmap(15, 15)), '')
        message_clear_bottom.setFlat(True)
        message_clear_bottom.setFixedHeight(22)
        message_clear_bottom.setFixedWidth(22)
        message_clear_bottom.clicked.connect(self.message_clear)
        messages_pane.tabBar().setTabButton(0, QTabBar.RightSide, message_clear_bottom)

        # Serial窗口添加按钮
        button_layout = QHBoxLayout()
        # setting
        serial_setting_bottom = QPushButton(QIcon(QIcon("icons/setting.svg").pixmap(15, 15)), '')
        serial_setting_bottom.setFlat(True)
        serial_setting_bottom.setFixedHeight(22)
        serial_setting_bottom.setFixedWidth(22)
        serial_setting_bottom.clicked.connect(self.serial_setting)
        button_layout.addWidget(serial_setting_bottom)
        # connect
        self.serial_connect_bottom = QPushButton(QIcon(QIcon("icons/connect.svg").pixmap(15, 15)), '')
        self.serial_connect_bottom.setFlat(True)
        self.serial_connect_bottom.setFixedHeight(22)
        self.serial_connect_bottom.setFixedWidth(22)
        self.serial_connect_bottom.clicked.connect(self.serial_connect)
        button_layout.addWidget(self.serial_connect_bottom)
        # disconnect
        self.serial_disconnect_bottom = QPushButton(QIcon(QIcon("icons/disconnect.svg").pixmap(15, 15)), '')
        self.serial_disconnect_bottom.setFlat(True)
        self.serial_disconnect_bottom.setFixedHeight(22)
        self.serial_disconnect_bottom.setFixedWidth(22)
        self.serial_disconnect_bottom.clicked.connect(self.serial_disconnect)
        self.serial_disconnect_bottom.setEnabled(False)
        button_layout.addWidget(self.serial_disconnect_bottom)
        # clear
        serial_clear_bottom = QPushButton(QIcon(QIcon("icons/clear.svg").pixmap(15, 15)), '')
        serial_clear_bottom.setFlat(True)
        serial_clear_bottom.setFixedHeight(22)
        serial_clear_bottom.setFixedWidth(22)
        serial_clear_bottom.clicked.connect(self.serial_clear)
        button_layout.addWidget(serial_clear_bottom)
        button_layout.setContentsMargins(0, 3, 0, 3)

        container = QWidget()
        container.setLayout(button_layout)
        messages_pane.tabBar().setTabButton(1, QTabBar.RightSide, container)


        # 设置上下窗格
        self.splitterr = QSplitter()
        self.splitterr.setOrientation(Qt.Vertical)
        self.splitterr.addWidget(content_pane)
        self.splitterr.addWidget(messages_pane)
        self.splitterr.setSizes([4, 1]) # 设置 edit_tab 和 simulation_tab 的大小比例
        # 设置左右窗格
        self.splitterl = QSplitter()
        self.splitterl.setOrientation(Qt.Horizontal)
        self.splitterl.addWidget(self.fileTree)
        self.splitterl.addWidget(self.splitterr)
        self.splitterl.setSizes([1, 8]) # 设置 edit_tab 和 simulation_tab 的大小比例
        self.splitterl.splitterMoved.connect(self.adjust_tablewidth)
        # 创建主窗口
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        splitter_layout = QVBoxLayout(main_widget)
        splitter_layout.addWidget(self.splitterl)  # 将QSplitter添加到布局中
        main_widget.setLayout(splitter_layout)


    def menu(self):
        # 文件菜单
        file_Menu = self.menuBar().addMenu('File')

        # 文件设置
        new_Action = QAction(QIcon('icons/new.svg'), 'New', self) # 新建文件
        new_Action.setToolTip('New')
        # new_Action.setShortcut('Ctrl+N') # 设置快捷键
        new_Action.triggered.connect(self.newFile)
        file_Menu.addAction(new_Action)

        # 添加新建项目的操作
        new_project_Action = QAction(QIcon('icons/newprogram.svg'), 'New Project', self) # 新建项目
        new_project_Action.setToolTip('New Project')
        # new_project_Action.setShortcut('Ctrl+P') # 设置快捷键
        new_project_Action.triggered.connect(self.newProject)
        file_Menu.addAction(new_project_Action)

        open_Action = QAction(QIcon('icons/openfolder.svg'), 'Open', self) # 打开动作
        open_Action.setToolTip('Open')
        # open_Action.setShortcut('Ctrl+O')  # 设置快捷键
        open_Action.triggered.connect(self.openFile)
        file_Menu.addAction(open_Action)

        open_folder_Action = QAction(QIcon('icons/openfolder.svg'), 'Open Folder', self) # 打开动作
        open_folder_Action.setToolTip('Open Folder')
        # open_folder_Action.setShortcut('Ctrl+F')  # 设置快捷键
        open_folder_Action.triggered.connect(self.openFolder)
        file_Menu.addAction(open_folder_Action)

        close_Action = QAction(QIcon('icons/close.svg'), 'Close', self) # 关闭动作
        close_Action.setToolTip('Close')
        # close_Action.setShortcut('Ctrl+W') # 设置快捷键
        close_Action.triggered.connect(self.closeFile)
        file_Menu.addAction(close_Action)

        closeall_Action = QAction('Close All', self) # 关闭所有动作
        # closeall_Action.setShortcut('Ctrl+Shift+W') # 设置快捷键
        closeall_Action.triggered.connect(self.closeAllFiles)
        file_Menu.addAction(closeall_Action)

        file_Menu.addSeparator()  # 分隔线

        save_Action = QAction(QIcon('icons/save.svg'), 'Save', self) # 保存动作
        save_Action.setToolTip('Save')
        save_Action.setShortcut('Ctrl+S')  # 设置快捷键
        save_Action.triggered.connect(self.saveFile)
        file_Menu.addAction(save_Action)

        saveas_Action = QAction('Save As...', self) # 另存动作
        # saveas_Action.setShortcut('Ctrl+Shift+S') # 设置快捷键
        saveas_Action.triggered.connect(self.saveasFile)
        file_Menu.addAction(saveas_Action)

        saveall_Action = QAction('Save All', self) # 全部保存
        # saveall_Action.setShortcut('Ctrl+Alt+S') # 设置快捷键
        saveall_Action.triggered.connect(self.saveAllFiles)
        file_Menu.addAction(saveall_Action)

        file_Menu.addSeparator()  # 分隔线

        exit_Action = QAction(QIcon('icons/exit.svg'), 'Exit', self) # 退出动作
        exit_Action.setToolTip('Exit')
        # exit_Action.setShortcut('Ctrl+Q')  # 设置快捷键
        exit_Action.triggered.connect(self.close)
        file_Menu.addAction(exit_Action)

        # 编辑菜单
        edit_Menu = self.menuBar().addMenu('Edit')

        undo_Action = QAction(QIcon('icons/undo.svg'), 'Undo', self) # 撤销操作
        undo_Action.setToolTip('Undo')
        # undo_Action.setShortcut('Ctrl+Z')  # 设置快捷键
        undo_Action.triggered.connect(self.undo)
        edit_Menu.addAction(undo_Action)

        redo_Action = QAction(QIcon('icons/redo.svg'), 'Redo', self) # 重做操作
        redo_Action.setToolTip('Redo')
        # redo_Action.setShortcut('Ctrl+Y')  # 设置快捷键
        redo_Action.triggered.connect(self.redo)
        edit_Menu.addAction(redo_Action)

        edit_Menu.addSeparator()  # 分隔线

        cut_Action = QAction(QIcon('icons/cut.svg'), 'Cut', self) # 剪切操作
        cut_Action.setToolTip('Cut')
        # cut_Action.setShortcut('Ctrl+X')  # 设置快捷键
        cut_Action.triggered.connect(self.cut)
        edit_Menu.addAction(cut_Action)

        copy_Action = QAction(QIcon('icons/copy.svg'), 'Copy', self) # 复制操作
        copy_Action.setToolTip('Copy')
        # copy_Action.setShortcut('Ctrl+C')  # 设置快捷键
        copy_Action.triggered.connect(self.copy)
        edit_Menu.addAction(copy_Action)

        paste_Action = QAction(QIcon('icons/paste.svg'), 'Paste', self) # 粘贴操作
        paste_Action.setToolTip('Paste')
        # paste_Action.setShortcut('Ctrl+V')  # 设置快捷键
        paste_Action.triggered.connect(self.paste)
        edit_Menu.addAction(paste_Action)

        # 运行菜单
        run_Menu = self.menuBar().addMenu('Run')

        assemble_Action = QAction(QIcon('icons/assemble.svg'), 'Assemble', self) # 编译
        assemble_Action.setToolTip('Assemble')
        # assemble_Action.setShortcut('Ctrl+R')  # 设置快捷键
        assemble_Action.triggered.connect(self.assemble)
        run_Menu.addAction(assemble_Action)

        clean_Action = QAction(QIcon('icons/clean.svg'), 'Clean', self) # 编译
        clean_Action.setToolTip('Assemble')
        # clean_Action.setShortcut('Ctrl+R')  # 设置快捷键
        clean_Action.triggered.connect(self.clean)
        run_Menu.addAction(clean_Action)

        self.connect_Action = QAction(QIcon("icons/connect.svg"), 'Connect', self) # 连接
        self.connect_Action.setToolTip('Connect')
        self.connect_Action.triggered.connect(self.connect)
        # self.connect_Action.setEnabled(False)
        run_Menu.addAction(self.connect_Action)

        self.disconnect_Action = QAction(QIcon("icons/disconnect.svg"), 'Disconnect', self) # 断开连接
        self.disconnect_Action.setToolTip('Disconnect')
        self.disconnect_Action.triggered.connect(self.disconnect)
        self.disconnect_Action.setEnabled(False)
        run_Menu.addAction(self.disconnect_Action)

        self.download_Action = QAction(QIcon("icons/download.svg"), 'Download', self) # 烧录
        self.download_Action.setToolTip('Download')
        self.download_Action.triggered.connect(self.download)
        self.download_Action.setEnabled(False)
        run_Menu.addAction(self.download_Action)

        self.stop_Action = QAction(QIcon("icons/stop.svg"), 'Run', self) # 烧录
        self.stop_Action.setToolTip('Stop')
        self.stop_Action.triggered.connect(self.stop_run)
        self.stop_Action.setEnabled(False)
        run_Menu.addAction(self.stop_Action)

        # 仿真菜单
        simulation_Menu = self.menuBar().addMenu('Simultion')

        self.simulation_stop_Action = QAction(QIcon('icons/run.svg'), 'Run', self) # 运行代码
        self.simulation_stop_Action.setToolTip('Run')
        self.simulation_stop_Action.triggered.connect(self.simulation_run)
        # self.stop_Action.setEnabled(False)
        simulation_Menu.addAction(self.simulation_stop_Action)

        self.simulation_run_step_Action = QAction(QIcon(QIcon('icons/run_step.svg').pixmap(22, 22)), 'Run step', self) # 单步运行
        self.simulation_run_step_Action.setToolTip('Run step')
        self.simulation_run_step_Action.triggered.connect(self.simulation_run_step)
        # self.run_step_Action.setEnabled(False)
        simulation_Menu.addAction(self.simulation_run_step_Action)

        self.simulation_run_undo_Action = QAction(QIcon(QIcon('icons/run_step.svg').pixmap(22, 22).transformed(QTransform().scale(-1, 1))), 'Run undo', self) # 单步退回
        self.simulation_run_undo_Action.setToolTip('Run undo')
        self.simulation_run_undo_Action.triggered.connect(self.simulation_run_undo)
        # self.run_undo_Action.setEnabled(False)
        simulation_Menu.addAction(self.simulation_run_undo_Action)

        self.simulation_reset_Action = QAction(QIcon('icons/reset.svg'), 'Reset', self) # 重启
        self.simulation_reset_Action.setToolTip('Reset')
        self.simulation_reset_Action.triggered.connect(self.simulation_reset)
        # self.reset_Action.setEnabled(False)
        simulation_Menu.addAction(self.simulation_reset_Action)

        self.simulation_stop_Action = QAction(QIcon('icons/stop.svg'), 'Stop', self) # 停止运行
        self.simulation_stop_Action.setToolTip('Stop')
        self.simulation_stop_Action.triggered.connect(self.simulation_stop)
        # self.stop_Action.setEnabled(False)
        simulation_Menu.addAction(self.simulation_stop_Action)

        # 调试菜单
        debug_Menu = self.menuBar().addMenu('Debug')

        self.debug_stop_Action = QAction(QIcon('icons/run.svg'), 'Run', self) # 运行代码
        self.debug_stop_Action.setToolTip('Run')
        self.debug_stop_Action.triggered.connect(self.debug_run)
        # self.stop_Action.setEnabled(False)
        debug_Menu.addAction(self.debug_stop_Action)

        self.debug_run_step_Action = QAction(QIcon(QIcon('icons/run_step.svg').pixmap(22, 22)), 'Run step', self) # 单步运行
        self.debug_run_step_Action.setToolTip('Run step')
        self.debug_run_step_Action.triggered.connect(self.debug_run_step)
        # self.run_step_Action.setEnabled(False)
        debug_Menu.addAction(self.debug_run_step_Action)

        self.debug_run_undo_Action = QAction(QIcon(QIcon('icons/run_step.svg').pixmap(22, 22).transformed(QTransform().scale(-1, 1))), 'Run undo', self) # 单步退回
        self.debug_run_undo_Action.setToolTip('Run undo')
        self.debug_run_undo_Action.triggered.connect(self.debug_run_undo)
        # self.run_undo_Action.setEnabled(False)
        debug_Menu.addAction(self.debug_run_undo_Action)

        self.debug_reset_Action = QAction(QIcon('icons/reset.svg'), 'Reset', self) # 重启
        self.debug_reset_Action.setToolTip('Reset')
        self.debug_reset_Action.triggered.connect(self.debug_reset)
        # self.reset_Action.setEnabled(False)
        debug_Menu.addAction(self.debug_reset_Action)

        self.debug_stop_Action = QAction(QIcon('icons/stop.svg'), 'Stop', self) # 停止运行
        self.debug_stop_Action.setToolTip('Stop')
        self.debug_stop_Action.triggered.connect(self.debug_stop)
        # self.stop_Action.setEnabled(False)
        debug_Menu.addAction(self.debug_stop_Action)

        # 帮助菜单
        help_Menu = self.menuBar().addMenu('Help')

        about_Action = QAction('About', self) # 关于
        about_Action.setToolTip('About')
        about_Action.triggered.connect(self.about)
        help_Menu.addAction(about_Action)


        # 工具栏
        toolbar1 = self.addToolBar('Toolbar1')
        toolbar1.addAction(new_Action)
        toolbar1.addAction(new_project_Action)
        toolbar1.addAction(open_folder_Action)
        toolbar1.addAction(close_Action)
        toolbar1.addAction(save_Action)

        toolbar2 = self.addToolBar('Toolbar2')
        toolbar2.addAction(undo_Action)
        toolbar2.addAction(redo_Action)
        toolbar2.addAction(cut_Action)
        toolbar2.addAction(copy_Action)
        toolbar2.addAction(paste_Action)

        toolbar3 = self.addToolBar('Toolbar3')
        toolbar3.addAction(assemble_Action)
        toolbar3.addAction(clean_Action)
        toolbar3.addAction(self.connect_Action)
        toolbar3.addAction(self.disconnect_Action)
        toolbar3.addAction(self.download_Action)
        toolbar3.addAction(self.stop_Action)

        toolbar4 = self.addToolBar('Toolbar4')
        toolbar4.addAction(self.simulation_stop_Action)
        toolbar4.addAction(self.simulation_run_step_Action)
        toolbar4.addAction(self.simulation_run_undo_Action)
        toolbar4.addAction(self.simulation_reset_Action)
        toolbar4.addAction(self.simulation_stop_Action)

        # 添加其他工具栏项...

    def table_init(self):
        # 设置表格只读
        self.simulation_code_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.simulation_label_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.simulation_data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.simulation_register_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.debug_code_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.debug_label_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.debug_data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.debug_register_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 设置表头
        self.simulation_code_table.setHorizontalHeaderLabels(["Address", "Code", "Source"])
        self.simulation_label_table.setHorizontalHeaderLabels(["Label", "Address"])
        self.simulation_data_table.setHorizontalHeaderLabels(["Address", "Value(+0)", "Value(+1)", "Value(+2)", "Value(+3)", "Value(+4)", "Value(+5)", "Value(+6)", "Value(+7)"])
        self.simulation_register_table.setHorizontalHeaderLabels(["Register", "Value"])
        self.debug_code_table.setHorizontalHeaderLabels(["Address", "Code", "Source"])
        self.debug_label_table.setHorizontalHeaderLabels(["Label", "Address"])
        self.debug_data_table.setHorizontalHeaderLabels(["Address", "Value(+0)", "Value(+1)", "Value(+2)", "Value(+3)", "Value(+4)", "Value(+5)", "Value(+6)", "Value(+7)"])
        self.debug_register_table.setHorizontalHeaderLabels(["Register", "Value"])

        # 设置表格不显示行号
        self.simulation_code_table.verticalHeader().setVisible(False)
        self.simulation_label_table.verticalHeader().setVisible(False)
        self.simulation_data_table.verticalHeader().setVisible(False)
        self.simulation_register_table.verticalHeader().setVisible(False)
        self.debug_code_table.verticalHeader().setVisible(False)
        self.debug_label_table.verticalHeader().setVisible(False)
        self.debug_data_table.verticalHeader().setVisible(False)
        self.debug_register_table.verticalHeader().setVisible(False)

        # 设置表格列宽
        self.set_ColumnWidth(self.simulation_code_table, 9)
        self.set_ColumnWidth(self.simulation_label_table, 8)
        self.set_ColumnWidth(self.simulation_data_table, 8)
        self.set_ColumnWidth(self.simulation_register_table, 8)
        self.set_ColumnWidth(self.debug_code_table, 9)
        self.set_ColumnWidth(self.debug_label_table, 8)
        self.set_ColumnWidth(self.debug_data_table, 8)
        self.set_ColumnWidth(self.debug_register_table, 8)

        # 设置表格行高
        self.set_RowWidth()

        # 设置 simulation_code_table 表格初值
        for row in range(self.simulation_code_table.rowCount()):
            for col in range(self.simulation_code_table.columnCount()):
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.simulation_code_table.setItem(row, col, item)
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.debug_code_table.setItem(row, col, item)

        # 设置 simulation_label_table 表格初值
        for row in range(self.simulation_label_table.rowCount()):
            for col in range(self.simulation_label_table.columnCount()):
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.simulation_label_table.setItem(row, col, item)
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.debug_label_table.setItem(row, col, item)

        # 设置 simulation_data_table 表格初值
        data_index = 0
        for row in range(self.simulation_data_table.rowCount()):
            for col in range(self.simulation_data_table.columnCount()):
                if col == 0:
                    address = "0x{:08X}".format(data_index*8)
                    item = QTableWidgetItem(address)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.simulation_data_table.setItem(row, col, item)
                    item = QTableWidgetItem(address)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.debug_data_table.setItem(row, col, item)
                    data_index += 1
                else:
                    item = QTableWidgetItem('00000000')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.simulation_data_table.setItem(row, col, item)
                    item = QTableWidgetItem('00000000')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.debug_data_table.setItem(row, col, item)

        # 设置 simulation_register_table 表格初值
        register_names = [
            "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
            "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
            "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
            "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"
        ]
        for row, register in enumerate(register_names):
            for col in range(self.simulation_register_table.columnCount()):
                item = QTableWidgetItem(register if col == 0 else "00000000")
                item.setTextAlignment(Qt.AlignCenter)
                self.simulation_register_table.setItem(row, col, item)
                item = QTableWidgetItem(register if col == 0 else "00000000")
                item.setTextAlignment(Qt.AlignCenter)
                self.debug_register_table.setItem(row, col, item)

        # 设置奇数行背景颜色为天蓝色，偶数行背景颜色为钢蓝色
        for tabel in [self.simulation_code_table, self.simulation_label_table, self.simulation_data_table, self.simulation_register_table]:
            for row in range(tabel.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)
        for tabel in [self.debug_code_table, self.debug_label_table, self.debug_data_table, self.debug_register_table]:
            for row in range(tabel.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)
        # 设置表格头部背景颜色
        self.simulation_code_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.simulation_label_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.simulation_data_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.simulation_register_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.debug_code_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.debug_label_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.debug_data_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")
        self.debug_register_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #C0B3B1; }")

    def setRowBackgroundColor(self, tabel, row, color):
        if row % 2 == 0:
            for col in range(tabel.columnCount()):
                item = tabel.item(row, col)
                if item is not None:
                    if color:
                        item.setBackground(color)
                    else:
                        item.setBackground(QColor("#8CBAB7")) # Light skyblue
        else:
            for col in range(tabel.columnCount()):
                item = tabel.item(row, col)
                if item is not None:
                    if color:
                        item.setBackground(color)
                    else:
                        item.setBackground(QColor("#D1A7A4")) # light steelblue

    def set_RowWidth(self):
        for table_widget in [self.simulation_label_table, self.simulation_register_table, self.simulation_code_table, self.simulation_data_table]:
            for row in range(table_widget.rowCount()):
                table_widget.setRowHeight(row, 32)
        for table_widget in [self.debug_label_table, self.debug_register_table, self.debug_code_table, self.debug_data_table]:
            for row in range(table_widget.rowCount()):
                table_widget.setRowHeight(row, 32)

    def set_ColumnWidth(self, table, line_num):
        if table == self.simulation_code_table:
            self.simulation_code_table.setColumnWidth(0, 275)  # Address
            self.simulation_code_table.setColumnWidth(1, 275)  # Code
            self.simulation_code_table.setColumnWidth(2, 540)  # Source
        elif table == self.simulation_label_table:
            self.simulation_label_table.setColumnWidth(0, 170)  # Label
            self.simulation_label_table.setColumnWidth(1, 175)  # Address
        elif table == self.simulation_data_table:
            for row in range(self.simulation_data_table.rowCount()):
                self.simulation_data_table.setColumnWidth(row, 121)  # Address
        elif table == self.simulation_register_table:
            self.simulation_register_table.setColumnWidth(0, 170)  # Register
            self.simulation_register_table.setColumnWidth(1, 175)  # Name
        if table == self.debug_code_table:
            self.debug_code_table.setColumnWidth(0, 275)  # Address
            self.debug_code_table.setColumnWidth(1, 275)  # Code
            self.debug_code_table.setColumnWidth(2, 540)  # Source
        elif table == self.debug_label_table:
            self.debug_label_table.setColumnWidth(0, 170)  # Label
            self.debug_label_table.setColumnWidth(1, 175)  # Address
        elif table == self.debug_data_table:
            for row in range(self.debug_data_table.rowCount()):
                self.debug_data_table.setColumnWidth(row, 121)  # Address
        elif table == self.debug_register_table:
            self.debug_register_table.setColumnWidth(0, 170)  # Register
            self.debug_register_table.setColumnWidth(1, 175)  # Name

    def adjust_tablewidth(self):
        # 获取分隔条两边的宽度
        widths = self.splitterl.sizes()
        left_width = widths[0]
        right_width = widths[1]
        # 计算每个列的宽度，使其适应表格宽度
        self.simulation_code_table.setColumnWidth(0, int((right_width-70)/4*3*0.25))  # Address
        self.simulation_code_table.setColumnWidth(1, int((right_width-70)/4*3*0.25))  # Code
        self.simulation_code_table.setColumnWidth(2, int((right_width-70)/4*3*0.5))  # Source
        self.debug_code_table.setColumnWidth(0, int((right_width-70)/4*3*0.25))  # Address
        self.debug_code_table.setColumnWidth(1, int((right_width-70)/4*3*0.25))  # Code
        self.debug_code_table.setColumnWidth(2, int((right_width-70)/4*3*0.5))  # Source
        for row in range(self.simulation_data_table.rowCount()): # Address
            self.simulation_data_table.setColumnWidth(row, int((right_width-70)/4*3/9))
            self.debug_data_table.setColumnWidth(row, int((right_width-70)/4*3/9))
        self.simulation_label_table.setColumnWidth(0, int((right_width-130)/4*1*0.5))  # Label
        self.simulation_label_table.setColumnWidth(1, int((right_width-130)/4*1*0.5))  # Address
        self.debug_label_table.setColumnWidth(0, int((right_width-130)/4*1*0.5))  # Label
        self.debug_label_table.setColumnWidth(1, int((right_width-130)/4*1*0.5))  # Address
        self.simulation_register_table.setColumnWidth(0, int((right_width-130)/4*1*0.5))  # Register
        self.simulation_register_table.setColumnWidth(1, int((right_width-130)/4*1*0.5))  # Name
        self.debug_register_table.setColumnWidth(0, int((right_width-130)/4*1*0.5))  # Register
        self.debug_register_table.setColumnWidth(1, int((right_width-130)/4*1*0.5))  # Name

    def loadFileDir(self, index):
        filePath = self.model.filePath(index)
        if os.path.isfile(filePath):
            # 创建新的文本编辑器选项卡
            text_edit = QTextEdit(self)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-image: url('icons/new.png');
                    background-repeat: no-repeat;
                    background-position: center;
                }
            """)
            text_edit.file_path = filePath  # 设置文件路径属性
            self.edit_area.addTab(text_edit, filePath.split("/")[-1])
            # 读取文件内容并显示在文本编辑器中
            try:
                with open(filePath, 'r', encoding='utf-8') as file:
                    text_edit.setPlainText(file.read())
            except UnicodeDecodeError:
                print("文件不是 UTF-8 编码，请尝试其他编码格式。")
            # 切换到新创建的选项卡
            index = self.edit_area.indexOf(text_edit)
            self.edit_area.setCurrentIndex(index)
        elif os.path.isdir(filePath):
            Workspace_Path = "/mnt/hgfs/share/Riscv-SoC-Software/Workspace"
            # 获取 filePath 的绝对路径
            parent_directory = os.path.dirname(filePath)
            # 判断 filePath 是否在 Workspace_Path 目录下
            if parent_directory == Workspace_Path:
                # print(f"{filePath} 位于 {Workspace_Path} 目录下")
                self.switchfolder(filePath)

    def newFile(self, start_page=False):
        # 创建新的文本编辑器选项卡
        text_edit = QTextEdit(self)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-image: url('icons/new.png');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)
        if start_page:
            self.edit_area.addTab(text_edit, "Gowin")
        else:
            self.edit_area.addTab(text_edit, "Untitled")
        # 切换到新创建的选项卡
        index = self.edit_area.indexOf(text_edit)
        self.edit_area.setCurrentIndex(index)

    def newProject(self):
        # 打开新建项目对话框
        new_project = NewPro()
        if new_project.exec_() == QDialog.Accepted:  # QDialog.Accepted 若用户点击了确定按钮
            self.switchfolder(new_project.project_path)

    def openFile(self):
        # 打开文件对话框
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "Text Files (*.txt);;All Files (*)", options=options)
        if not file_paths:  # 如果没有选择文件
            print("没有选择文件")
            return  # 直接返回，不执行后续代码
        for file_path in file_paths:
            if file_path:
                print(f"打开文件: {file_path}")
                # 创建新的文本编辑器选项卡
                text_edit = QTextEdit(self)
                text_edit.file_path = file_path  # 设置文件路径属性
                self.edit_area.addTab(text_edit, file_path.split("/")[-1])
                # 读取文件内容并显示在文本编辑器中
                with open(file_path, 'r') as file:
                    text_edit.setPlainText(file.read())

    def switchfolder(self, path):
        # 切换文件夹
        self.project_path = path
        self.project_name = self.project_path.split('/')[-1]
        self.fileTree.setRootIndex(self.model.index(self.project_path))
        try:
            self.fillfile()
        except:
            pass
        try:
            self.fillCode()
        except:
            pass
        try:
            self.fillLabel()
        except:
            pass
        try:
            self.Sim.load_program(self.project_path + f"/build/{self.project_name}.v")
        except:
            pass
        # 设置奇数行背景颜色为天蓝色，偶数行背景颜色为钢蓝色
        for tabel in [self.simulation_code_table, self.simulation_label_table, self.simulation_data_table, self.simulation_register_table]:
            for row in range(self.simulation_code_table.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)
        for tabel in [self.debug_code_table, self.debug_label_table, self.debug_data_table, self.debug_register_table]:
            for row in range(tabel.rowCount()):
                self.setRowBackgroundColor(tabel, row, None)

    def openFolder(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Open Folder', '/mnt/hgfs/share/Riscv-SoC-Software/Workspace')
        if dirName:
            self.switchfolder(dirName)

    def addFileToEditArea(self, filePath):
        # 创建新的标签页
        new_tab = QWidget()
        new_layout = QVBoxLayout(new_tab)
        # 创建 QTextEdit 并加载文件内容
        editor_area = QTextEdit()
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
            editor_area.setPlainText(content)
        new_layout.addWidget(editor_area)
        # 将新标签页添加到 edit_area
        self.edit_area.addTab(new_tab, os.path.basename(filePath))
        self.edit_area.setCurrentWidget(new_tab)  # 切换到新标签页

    def closeFile(self):
        # 获取当前活动的选项卡索引
        current_index = self.edit_area.currentIndex()
        # 关闭当前选项卡
        if current_index != -1:
            self.edit_area.removeTab(current_index)

    def closeAllFiles(self):
        # 关闭所有选项卡
        self.edit_area.clear()

    def saveFile(self):
        # 获取当前活动的选项卡
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        # 获取当前文件路径
        file_path = getattr(current_tab, 'file_path', None)
        # 如果没有文件路径，则调用另存为逻辑
        if not file_path:
            self.saveasFile()
            return
        # 将当前选项卡的文本编辑器内容保存到文件中
        if current_tab and file_path:
            with open(file_path, 'w') as file:
                file.write(current_tab.toPlainText())

    def saveasFile(self):
        # 获取当前活动的选项卡
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        # 处理另存为文件逻辑
        if current_tab:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)", options=options)
            if fileName:
                with open(fileName, 'w') as file:
                    file.write(current_tab.toPlainText())

    def saveAllFiles(self):
        # 迭代所有已打开的文件并保存它们
        for index in range(self.edit_area.count()):
            current_tab = self.edit_area.widget(index)
            file_path = getattr(current_tab, 'file_path', None)
            if current_tab and file_path:
                with open(file_path, 'w') as file:
                    file.write(current_tab.toPlainText())

    def undo(self):
        # 处理撤销逻辑
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        if current_tab:
            current_tab.undo()

    def redo(self):
        # 处理重做逻辑
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        if current_tab:
            current_tab.redo()

    def cut(self):
        # 处理剪切逻辑
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        if current_tab:
            current_tab.cut()

    def copy(self):
        # 处理复制逻辑
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        if current_tab:
            current_tab.copy()

    def paste(self):
        # 处理粘贴逻辑
        current_index = self.edit_area.currentIndex()
        current_tab = self.edit_area.widget(current_index)
        if current_tab:
            current_tab.paste()

    # Python程序从Intel HEX文件中读取RISC-V指令并列出a
    def parse_hex_line(self, line):
        """
        解析一行Intel HEX文件 ， 返回一个元组 (数据长度, 地址, 记录类型, 数据)。，，，，，，，，，，，，
        """
        line = line.strip()
        if line[0] != ':':
            raise ValueError("Invalid HEX line")

        byte_count = int(line[1:3], 16)
        address = int(line[3:7], 16)
        record_type = int(line[7:9], 16)
        data = line[9:9 + byte_count * 2]
        checksum = int(line[9 + byte_count * 2:], 16)

        return address, record_type, data

    def extract_machinecode(self, file_path):
        """
        从Intel HEX文件中读取数据，并返回包含RISC-V程序指令的列表。
        """
        instructions = []
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    address, record_type, data = self.parse_hex_line(line)
                    # 我们只关心数据记录类型（通常为0）
                    if record_type == 0:
                        # 将16进制数据分成4字节的RISC-V指令
                        for i in range(0, len(data), 8):  # 8个字符是4字节（32位）的指令
                            instruction = data[i:i+8]
                            instructions.append(instruction)
                            address += 4  # RISC-V指令是32位(4字节)，地址每次增加4

                except ValueError as e:
                    print(f"Skipping invalid line: {line}")

        return "\n".join(instructions)

    def extract_assemblecode(self, file_path):
        assemble_code = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # 判断当前行是否以"80"开头
                    if line.startswith("80") and not line.endswith(":\n"):
                        # 将符合条件的行追加到结果字符串中
                        assemble_code += line.replace("          	", "    ")
                return assemble_code
        except:
            pass

    def extract_Label(self, file_path):
        Label = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # 判断当前行是否以"80"开头
                    if line.startswith("80") and line.endswith(":\n"):
                        # 将符合条件的行追加到结果字符串中
                        Label += line
                return Label
        except:
            pass

    def fillfile(self):
        try:
            assemble_path = self.project_path + f"/build/{self.project_name}.asm"
            self.assemble_code_area.setPlainText(self.extract_assemblecode(assemble_path))
            machine_path = self.project_path + f"/build/{self.project_name}.hex"
            self.machine_code_area.setPlainText(self.extract_machinecode(machine_path))
        except:
            pass

    def assemble(self):
        try:
            # 使用 "make clean && make" 命令
            make = subprocess.Popen("make clean && make", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.project_path)
            stdout, stderr = make.communicate()
            if stdout:
                stdout_lines = stdout.decode('utf-8').splitlines()  # 将输出按行分割
                last_three_lines = "\n".join(stdout_lines[-3:])  # 取最后三行
                self.message_showmessage(last_three_lines + "\n")
                self.fillfile()
                self.fillCode()
                self.fillLabel()
                # 设置奇数行背景颜色为天蓝色，偶数行背景颜色为钢蓝色
                for tabel in [self.simulation_code_table, self.simulation_label_table, self.simulation_data_table, self.simulation_register_table]:
                    for row in range(self.simulation_code_table.rowCount()):
                        self.setRowBackgroundColor(tabel, row, None)
                for tabel in [self.debug_code_table, self.debug_label_table, self.debug_data_table, self.debug_register_table]:
                    for row in range(tabel.rowCount()):
                        self.setRowBackgroundColor(tabel, row, None)
        except subprocess.CalledProcessError as e:
            print(e)

    def clean(self):
        try:
            shutil.rmtree(self.project_path + "/build")
            self.message_showmessage("rm -rf ./build\nClear Project...")
            self.assemble_code_area.clear()
            self.machine_code_area.clear()
        except Exception as e:
            print(e)

    def connect(self):
        if self.openocd_process is None:
            self.message_showmessage('Openocd connecting...')
            try:
                # 运行 openocd 并将其放入后台
                self.openocd_process = subprocess.Popen(
                    ['/home/moon/openocd_riscv/src/openocd', '-f', '/mnt/hgfs/share/Riscv-SoC-Software/scripts/cyber.cfg'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp
                )
                # self.message_showmessage('Openocd: connected successed.')
                self.connect_Action.setEnabled(False)
                self.disconnect_Action.setEnabled(True)
                self.download_Action.setEnabled(True)
            except Exception as e:
                self.message_showmessage(f'Openocd: connected failed-{str(e)}')
        else:
            self.message_showmessage('openocd already running in the background')

    def disconnect(self):
        if self.openocd_process is not None:
            try:
                # 结束 openocd 进程
                os.killpg(os.getpgid(self.openocd_process.pid), signal.SIGTERM)
                self.openocd_process = None
                self.message_showmessage('Openocd disconnected.')
                self.connect_Action.setEnabled(True)
                self.disconnect_Action.setEnabled(False)
                self.download_Action.setEnabled(False)
                self.stop_Action.setEnabled(False)
            except Exception as e:
                self.message_showmessage(e)
        else:
            self.message_showmessage('Openocd not running.')

    def download(self):
        # 下载/烧录
        """ 当按钮被点击时，开始烧录过程 """
        program = f"{self.project_path}/build/{self.project_name}.elf"
        # 启动烧录的线程
        if os.path.exists(program):
            self.message_showmessage('Downloading ...')
            self.gdb_thread = GdbThread(self)
            self.gdb_thread.load_prog(program)
            self.gdb_thread.progress_signal.connect(self.update_status)
            # self.gdb_thread.finished.connect(self.on_finish)
            self.gdb_thread.start()
            self.download_Action.setEnabled(False)
            self.stop_Action.setEnabled(True)
        else:
            self.message_showmessage('Program do not exist!')

    def stop_run(self):
        self.gdb_thread.stop_run()
        self.download_Action.setEnabled(True)
        self.stop_Action.setEnabled(False)

    def update_status(self, message):
        """ 更新界面上的状态，并显示 GDB 输出 """
        self.message_showmessage(message)

    def simulation_run(self):
        # 运行程序
        try:
            self.Sim.load_program(self.project_path + f"/build/{self.project_name}.v")
            print(self.Sim.pyriscv._pc)
            self.setRowBackgroundColor(self.simulation_code_table, self.Sim.pc, QColor(200, 0, 0))
        except:
            pass

    def simulation_run_step(self):
        # 单步运行程序
        self.Sim.step()
        self.fillRegister(self.Sim.pyriscv._regs)
        # self.fillData(self.Sim.pyriscv._dmem)

        # 将运行到的行标红
        self.setRowBackgroundColor(self.simulation_code_table, self.Sim.pc / 4, QColor(255, 0, 0))
        self.setRowBackgroundColor(self.simulation_code_table, self.Sim.last_pc / 4, None)

    def simulation_run_undo(self):
        # 单步返回程序
        pass

    def simulation_reset(self):
        # 将表格颜色恢复到初值
        pass

    def simulation_stop(self):
        # 停止运行程序
        pass

    def fillCode(self):
        # 按行分割文本
        lines_assembly = list(filter(lambda line: line.strip() != "", self.assemble_code_area.toPlainText().split('\n'))) # 去除空行
        address = []
        machine = []
        assemble = []
        for line in lines_assembly:
            split_line = line.split(maxsplit=2)
            address.append(split_line[0][:-1])
            machine.append(split_line[1])
            assemble.append(split_line[2])
        # 设置表格的行数
        self.simulation_code_table.setRowCount(len(lines_assembly))
        self.debug_code_table.setRowCount(len(lines_assembly))
        for row in range(self.simulation_code_table.rowCount()):
            for col in range(self.simulation_code_table.columnCount()):
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.simulation_code_table.setItem(row, col, item)
                item = QTableWidgetItem('-')
                item.setTextAlignment(Qt.AlignCenter)
                self.debug_code_table.setItem(row, col, item)
        # 填入数据
        for row_index in range(len(lines_assembly)):
            # 填入地址
            self.simulation_code_table.item(row_index, 0).setText(address[row_index])
            self.debug_code_table.item(row_index, 0).setText(address[row_index])
            # 填入机械码
            self.simulation_code_table.item(row_index, 1).setText(machine[row_index])
            self.debug_code_table.item(row_index, 1).setText(machine[row_index])
            # 填入汇编码
            self.simulation_code_table.item(row_index, 2).setText(assemble[row_index])
            self.simulation_code_table.item(row_index, 2).setTextAlignment(int(Qt.AlignLeft | Qt.AlignVCenter))
            self.debug_code_table.item(row_index, 2).setText(assemble[row_index])
            self.debug_code_table.item(row_index, 2).setTextAlignment(int(Qt.AlignLeft | Qt.AlignVCenter))

    def fillLabel(self):
        try:
            assemble_path = self.project_path + f"/build/{self.project_name}.asm"
            self.Label = list(filter(lambda line: line.strip() != "", self.extract_Label(assemble_path).split('\n'))) # 去除空行
            # 设置表格的行数
            self.simulation_label_table.setRowCount(max(len(self.Label), 8))
            self.debug_label_table.setRowCount(max(len(self.Label), 8))
            for row in range(self.simulation_label_table.rowCount()):
                for col in range(self.simulation_label_table.columnCount()):
                    item = QTableWidgetItem('-')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.simulation_label_table.setItem(row, col, item)
                    item = QTableWidgetItem('-')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.debug_label_table.setItem(row, col, item)
            # 填充表格
            for index, line in enumerate(self.Label):
                address, label = line.split(maxsplit=1)
                label = label.strip('<>:')  # remove '<' '>' and ':' around '_start'
                self.simulation_label_table.item(index, 0).setText(label)
                self.simulation_label_table.item(index, 1).setText(address)
                self.debug_label_table.item(index, 0).setText(label)
                self.debug_label_table.item(index, 1).setText(address)
        except:
            pass

    def fillRegister(self, data):
        # 确保数据和表格行数匹配
        if len(data) != self.simulation_register_table.rowCount():
            raise ValueError("Data dimensions do not match table dimensions.")
        for row in range(len(data)):
            self.simulation_register_table.item(row, 1).setText("0x{:04X}".format(data[row]))

    def fillData(self, data):
        # 根据字典填充数据到表格
        pass

    def debug_run(self):
        # 运行程序
        pass

    def debug_run_step(self):
        # 单步运行程序
        pass

    def debug_run_undo(self):
        # 单步返回程序
        pass

    def debug_reset(self):
        # 将表格颜色恢复到初值
        pass

    def debug_stop(self):
        # 停止运行程序
        pass

    def about(self):
        # 关于
        about_text = "简单IDE v1.0\n\n一个基于PyQt的简单集成开发环境。\n\n作者: CyberMalo"
        QMessageBox.about(self, '关于', about_text)

    def message_showmessage(self, message):
        # 将内容添加到messages
        self.message_tab.append(message)

    def message_clear(self):
        # 清除message
        self.message_tab.setPlainText('')

    def serial_showmessage(self, message):
        # 将内容添加到messages
        current_content = self.message_tab.toPlainText()
        updated_content = current_content + message
        self.serial_tab.setPlainText(updated_content)

    def serial_setting(self):
        # 打开串口配置窗口
        if self.Serial.exec_() == QDialog.Accepted:
            # 配置串口
            pass

    def serial_connect(self):
        # 连接串口
        pass

    def serial_disconnect(self):
        self.download_Action.setEnabled(False)
        self.serial_connect_bottom.setEnabled(True)
        self.serial_disconnect_bottom.setEnabled(False)
        self.message_showmessage("Port  closed\n")

    def serial_clear(self):
        # 清除 serial message
        self.serial_tab.setPlainText('')

    def closeEvent(self, event):
        """ 在窗口关闭时自动断开连接 """
        self.disconnect()
        event.accept()  # 关闭窗口


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()  # 显示IDE窗口
    sys.exit(app.exec_())

import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QFrame, QCheckBox, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from GPIOConf import GPIOConf, GPIOConfigDialog, GPIOConfTable

class NewPro(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Project")
        self.setWindowIcon(QIcon('icons/app.svg'))
        self.resize(400, 250)  # 增加窗口宽度

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建项目名称输入标签和输入框
        project_name_layout = QHBoxLayout()
        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        project_name_layout.addWidget(self.project_name_label)
        project_name_layout.addWidget(self.project_name_input)
        main_layout.addLayout(project_name_layout)

        # 是否使用默认位置
        self.default_location_checkbox = QCheckBox("Use default location")
        self.default_location_checkbox.setChecked(True)
        self.default_location_checkbox.toggled.connect(self.toggle_location_input)
        self.browse_button = QPushButton("Browse")
        self.browse_button.setEnabled(False)
        self.browse_button.clicked.connect(self.browse_folder)
        location_layout = QHBoxLayout()
        location_layout.addWidget(self.default_location_checkbox)
        location_layout.addWidget(self.browse_button)
        main_layout.addLayout(location_layout)

        # 创建项目生成路径输入标签、输入框和按钮
        self.project_path_label = QLabel("Location:")
        self.project_path_input = QLineEdit()
        self.project_path_input.setEnabled(False)
        location_layout = QHBoxLayout()
        location_layout.addWidget(self.project_path_label)
        location_layout.addWidget(self.project_path_input)
        # location_layout.addWidget(self.browse_button)
        main_layout.addLayout(location_layout)

        # 横条：分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # 硬件部分
        self.hardware_label = QLabel("Hardware")
        main_layout.addWidget(self.hardware_label)
        # AHB 配置
        self.ahb_label = QLabel("AHB")
        self.ahb_checkbox = QCheckBox("Enable")
        self.ahb_checkbox.toggled.connect(self.toggle_ahb_config)
        self.ahb_button = QPushButton("Configration")
        self.ahb_button.clicked.connect(self.open_gpio_config)
        self.ahb_button.setEnabled(False)
        ahb_layout = QHBoxLayout()
        ahb_layout.addWidget(self.ahb_label)
        ahb_layout.addWidget(self.ahb_checkbox)
        ahb_layout.addWidget(self.ahb_button)
        main_layout.addLayout(ahb_layout)
        # APB 配置
        self.apb_label = QLabel("APB")
        self.apb_checkbox = QCheckBox("Enable")
        self.apb_checkbox.toggled.connect(self.toggle_ahb_config)
        self.apb_button = QPushButton("Configration")
        self.apb_button.clicked.connect(self.open_gpio_config)
        self.apb_button.setEnabled(False)
        apb_layout = QHBoxLayout()
        apb_layout.addWidget(self.apb_label)
        apb_layout.addWidget(self.apb_checkbox)
        apb_layout.addWidget(self.apb_button)
        main_layout.addLayout(apb_layout)

        # 横条：分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # 软件部分
        self.software_label = QLabel("Software")
        main_layout.addWidget(self.software_label)
        # 工程模板，子模板标签
        template_label = QLabel("Project Template:")
        sub_template_label = QLabel("Sub-Template:")
        template_layout = QHBoxLayout()
        template_layout.addWidget(template_label)
        template_layout.addWidget(sub_template_label)
        main_layout.addLayout(template_layout)
        # 工程模板和子模板下拉框
        self.template_combo = QComboBox()
        self.template_combo.addItems(["bare", "freertos", "rt-thread"])
        self.template_combo.currentIndexChanged.connect(self.update_options)
        self.sub_template_combo = QComboBox()
        self.update_options()
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.template_combo)
        combo_layout.addWidget(self.sub_template_combo)
        main_layout.addLayout(combo_layout)

        # 确认按钮
        self.confirm_button = QPushButton("confirm")
        self.confirm_button.clicked.connect(self.confirm)
        main_layout.addWidget(self.confirm_button)

        # 设置布局
        self.setLayout(main_layout)

    def browse_folder(self):
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # 如果选择了文件夹，则将路径显示到输入框
        if folder:
            self.project_path_input.setText(folder)

    def open_gpio_config(self):
        # 创建并显示 GPIO 配置对话框
        gpio_config_dialog = GPIOConfigDialog()
        gpio_config_dialog.exec_()  # 以模态方式显示对话框

    def toggle_location_input(self):
        # 控制位置输入框和浏览按钮的使能状态
        is_default = self.default_location_checkbox.isChecked()
        self.project_path_input.setEnabled(not is_default)
        self.browse_button.setEnabled(not is_default)

    def toggle_ahb_config(self):
        # 控制 AHB 配置按钮的使能状态
        self.ahb_button.setEnabled(self.ahb_checkbox.isChecked())
    
    def toggle_apb_config(self):
        # 控制 APB 配置按钮的使能状态
        self.apb_button.setEnabled(self.apb_checkbox.isChecked())
    
    def browse_location(self):
        # 打开文件对话框选择路径
        location = QFileDialog.getExistingDirectory(self, "Select Location")
        if location:
            self.location_input.setText(location)

    def update_options(self):
        # 获取第一个选择框的选中项
        selected_template = self.template_combo.currentText()
        # 清空当前的动态选择框内容
        self.sub_template_combo.clear()
        # 根据第一个选择框的选项生成第二个选择框的内容
        if selected_template == "bare":
            self.sub_template_combo.addItems(["boot", "demo", "dvp", "led_breathe", "led_flow"])
        elif selected_template == "freertos":
            self.sub_template_combo.addItems(["demo1-blinky", "test"])
        elif selected_template == "rt-thread":
            self.sub_template_combo.addItems([
                "demo1-thread", "demo2-container", "demo3-delay", "demo4-muti_priority",
                "demo5-timer", "demo6-timeslice", "demo7-finish", "demo7-finish+", "test"
            ])

    def confirm(self):
        self.project_path = self.project_path_input.text()
        selected_template = self.template_combo.currentText()

        # 复制模板工程到指定路径
        # if not os.path.exists(target_dir):
        #     os.makedirs(target_dir)  # 如果目标目录不存在，则创建它


        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NewPro()
    dialog.exec_()

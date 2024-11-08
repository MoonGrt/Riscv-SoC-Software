import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QCheckBox, QPushButton,
                             QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog, QFrame,
                             QSpacerItem, QSizePolicy)


class NewProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle('New Project')
        
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 第一行：项目名称
        project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        
        project_name_layout = QHBoxLayout()
        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(self.project_name_input)
        main_layout.addLayout(project_name_layout)
        
        # 第二行：是否使用默认位置
        self.default_location_checkbox = QCheckBox("Use default location")
        self.default_location_checkbox.stateChanged.connect(self.toggle_location_input)
        main_layout.addWidget(self.default_location_checkbox)
        
        # 第四行：位置，输入框和浏览按钮
        location_label = QLabel("Location:")
        self.location_input = QLineEdit()
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_location)
        
        # 默认禁用位置输入框和浏览按钮
        self.location_input.setEnabled(False)
        browse_button.setEnabled(False)
        
        location_layout = QHBoxLayout()
        location_layout.addWidget(location_label)
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_button)
        main_layout.addLayout(location_layout)
        
        # 第五行：空行
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 第六行：Hardware 标签
        hardware_label = QLabel("Hardware")
        main_layout.addWidget(hardware_label)
        
        # 第七行：CPU频率
        cpu_freq_label = QLabel("CPU Frequency:")
        self.cpu_freq_input = QLineEdit()
        
        cpu_freq_layout = QHBoxLayout()
        cpu_freq_layout.addWidget(cpu_freq_label)
        cpu_freq_layout.addWidget(self.cpu_freq_input)
        main_layout.addLayout(cpu_freq_layout)
        
        # 第八行：AHB配置
        self.ahb_checkbox = QCheckBox("Enable AHB Configuration")
        self.ahb_checkbox.stateChanged.connect(self.toggle_ahb_config)
        self.ahb_button = QPushButton("AHB Configuration")
        self.ahb_button.setEnabled(False)
        
        ahb_layout = QHBoxLayout()
        ahb_layout.addWidget(self.ahb_checkbox)
        ahb_layout.addWidget(self.ahb_button)
        main_layout.addLayout(ahb_layout)
        
        # 第九行：APB配置
        self.apb_checkbox = QCheckBox("Enable APB Configuration")
        self.apb_checkbox.stateChanged.connect(self.toggle_apb_config)
        self.apb_button = QPushButton("APB Configuration")
        self.apb_button.setEnabled(False)
        
        apb_layout = QHBoxLayout()
        apb_layout.addWidget(self.apb_checkbox)
        apb_layout.addWidget(self.apb_button)
        main_layout.addLayout(apb_layout)
        
        # 横条：分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 第十行：Software 标签
        software_label = QLabel("Software")
        main_layout.addWidget(software_label)
        
        # 第十一行：工程模板，子模板标签
        template_label = QLabel("Project Template:")
        sub_template_label = QLabel("Sub-Template:")
        
        template_layout = QHBoxLayout()
        template_layout.addWidget(template_label)
        template_layout.addWidget(sub_template_label)
        main_layout.addLayout(template_layout)
        
        # 第十二行：工程模板和子模板下拉框
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Template 1", "Template 2", "Template 3"])
        
        self.sub_template_combo = QComboBox()
        self.sub_template_combo.addItems(["Sub-Template A", "Sub-Template B", "Sub-Template C"])
        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.template_combo)
        combo_layout.addWidget(self.sub_template_combo)
        main_layout.addLayout(combo_layout)
        
        # 设置主布局
        self.setLayout(main_layout)
    
    def toggle_location_input(self):
        # 控制位置输入框和浏览按钮的使能状态
        is_default = self.default_location_checkbox.isChecked()
        self.location_input.setEnabled(not is_default)
        self.findChild(QPushButton, "Browse").setEnabled(not is_default)
    
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NewProjectDialog()
    dialog.exec_()

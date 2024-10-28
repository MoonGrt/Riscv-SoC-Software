import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)

class HardwareConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("硬件配置")
        layout = QVBoxLayout()

        # 设备信息示例
        self.device_info_label = QLabel("设备信息: 示例设备")
        layout.addWidget(self.device_info_label)

        self.setLayout(layout)

class NewProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("新建工程项目")

        layout = QVBoxLayout()

        # 项目生成路径输入
        self.project_path_label = QLabel("项目生成路径:")
        self.project_path_input = QLineEdit()
        layout.addWidget(self.project_path_label)
        layout.addWidget(self.project_path_input)

        # 硬件部分
        self.hardware_info_label = QLabel("硬件部分: 设备信息")
        self.hardware_config_button = QPushButton("配置硬件")
        self.hardware_config_button.clicked.connect(self.open_hardware_config)
        layout.addWidget(self.hardware_info_label)
        layout.addWidget(self.hardware_config_button)

        # 软件部分
        self.software_template_label = QLabel("选择模板工程:")
        self.template_combo = QComboBox()
        self.template_combo.addItems(["bare", "freertos", "rt-thread"])
        layout.addWidget(self.software_template_label)
        layout.addWidget(self.template_combo)

        # 确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def open_hardware_config(self):
        dialog = HardwareConfigDialog()
        dialog.exec_()

    def confirm(self):
        project_path = self.project_path_input.text()
        selected_template = self.template_combo.currentText()
        QMessageBox.information(self, "确认", f"项目路径: {project_path}\n选择的模板: {selected_template}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NewProjectDialog()
    dialog.exec_()

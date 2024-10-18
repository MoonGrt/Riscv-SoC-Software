import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox

class GPIOConfigurator(QWidget):
    def __init__(self, gpio_count=8):
        super().__init__()

        self.setWindowTitle("GPIO Configurator")
        self.layout = QVBoxLayout()

        # Store selected configurations
        self.gpio_configs = {}

        # Create GPIO selection for each pin
        for pin in range(gpio_count):
            pin_layout = QHBoxLayout()

            # GPIO Label
            gpio_label = QLabel(f"GPIO {pin}:")
            pin_layout.addWidget(gpio_label)

            # Dropdown for function selection
            gpio_select = QComboBox()
            gpio_select.addItems(["Timer", "I2C", "SPI", "GPIO", "WDG"])
            gpio_select.currentIndexChanged.connect(lambda idx, p=pin: self.update_gpio_config(p, idx))
            pin_layout.addWidget(gpio_select)

            self.layout.addLayout(pin_layout)

        # Generate button
        generate_button = QPushButton("Generate Verilog")
        generate_button.clicked.connect(self.generate_verilog)
        self.layout.addWidget(generate_button)

        self.setLayout(self.layout)

    def update_gpio_config(self, pin, index):
        """Update GPIO configuration based on user selection."""
        functions = ["Timer", "I2C", "SPI", "GPIO", "WDG"]
        self.gpio_configs[pin] = functions[index]

    def generate_verilog(self):
        """Generate Verilog code based on GPIO configurations."""
        verilog_code = "// Generated Verilog for GPIO Configuration\n"
        for pin, func in self.gpio_configs.items():
            verilog_code += f"// GPIO {pin} configured as {func}\n"
        QMessageBox.information(self, "Verilog Code", verilog_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIOConfigurator(gpio_count=8)
    window.show()
    sys.exit(app.exec_())

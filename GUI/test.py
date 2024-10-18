import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QGridLayout

class GpioMultiplexingConfigurator(QWidget):
    def __init__(self, gpio_count=16):
        super().__init__()
        
        self.setWindowTitle("GPIO Multiplexing Configurator")
        self.layout = QVBoxLayout()

        # Store GPIO configurations
        self.gpio_configs = {}

        # Create a grid layout for pin configuration
        grid_layout = QGridLayout()

        # Labels for the grid
        grid_layout.addWidget(QLabel("GPIO Pin"), 0, 0)
        grid_layout.addWidget(QLabel("Function"), 0, 1)

        # Add pin configuration options
        for pin in range(gpio_count):
            # Label for each GPIO pin
            gpio_label = QLabel(f"GPIO {pin}")
            grid_layout.addWidget(gpio_label, pin + 1, 0)

            # Dropdown for function selection
            gpio_select = QComboBox()
            gpio_select.addItems(["GPIO", "I2C", "SPI", "UART", "Timer", "PWM"])
            gpio_select.currentIndexChanged.connect(lambda idx, p=pin: self.update_gpio_config(p, idx))
            grid_layout.addWidget(gpio_select, pin + 1, 1)

            # Initialize configuration to default (GPIO)
            self.gpio_configs[pin] = "GPIO"

        # Add grid layout to the main layout
        self.layout.addLayout(grid_layout)

        # Generate button
        generate_button = QPushButton("Generate Verilog")
        generate_button.clicked.connect(self.generate_verilog)
        self.layout.addWidget(generate_button)

        self.setLayout(self.layout)

    def update_gpio_config(self, pin, index):
        """Update GPIO configuration based on user selection."""
        functions = ["GPIO", "I2C", "SPI", "UART", "Timer", "PWM"]
        self.gpio_configs[pin] = functions[index]

    def generate_verilog(self):
        """Generate Verilog code based on GPIO configurations."""
        verilog_code = "// Generated Verilog for GPIO Multiplexing Configuration\n"
        for pin, func in self.gpio_configs.items():
            verilog_code += f"// GPIO {pin} configured as {func}\n"

        # Show the generated code in a message box (or could save to file)
        QMessageBox.information(self, "Generated Verilog", verilog_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GpioMultiplexingConfigurator(gpio_count=16)
    window.show()
    sys.exit(app.exec_())

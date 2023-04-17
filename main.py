import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Example")
        self.setGeometry(100, 100, 300, 100)

        label = QLabel("Hello, PyQt6!", self)
        label.move(100, 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

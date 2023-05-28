import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QHBoxLayout
from set_style import SetStyle


class MainWindow(QMainWindow):
    options_signal = pyqtSignal(str)
    additional_signal = pyqtSignal(int)

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("답변 스타일 설정", self)
        self.button.setGeometry(50, 50, 200, 30)
        self.button.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.new_window = SetStyle()
        self.new_window.options_signal.connect(self.receive_value)  # 시그널과 슬롯 연결
        self.new_window.additional_signal.connect(self.additional_value)
        self.new_window.show()

    def receive_value(self, value):
        print("답변 스타일:", value)
    
    def additional_value(self, value):
        print("추천 질문 여부: ", value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

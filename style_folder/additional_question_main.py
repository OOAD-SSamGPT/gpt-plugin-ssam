import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from question_generator import Q_generator_by_GPT

# 어떻게 추가해야할지 잘 몰라서 텍스트 박스에 시뮬레이션 하는 것 처럼 했음..
# 추가질문은 3개로 설정함

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Q = Q_generator_by_GPT()

        self.setWindowTitle("추가 질문 생성")
        self.setGeometry(100, 100, 300, 200)

        self.button_layout = QVBoxLayout()

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.button_layout)
        self.setCentralWidget(self.central_widget)

        self.textbox = QLineEdit()
        self.textbox.returnPressed.connect(self.create_buttons)
        self.textbox.setPlaceholderText("마지막 답변 텍스트")
        self.button_layout.addWidget(self.textbox)

        self.buttons = []

    def create_buttons(self):
        sentence = self.textbox.text()
        Q_lst = self.Q.follow_questions(sentence, 3)
        if sentence:
            if len(self.buttons) >= 3:
                for i, button in enumerate(self.buttons):
                    button.setText(Q_lst[i])
            else:
                for i in range(3 - len(self.buttons)):
                    button = QPushButton(Q_lst[i])
                    button.clicked.connect(self.button_clicked)
                    self.buttons.append(button)
                    self.button_layout.addWidget(button)
        print(Q_lst)

    def button_clicked(self):
        button = self.sender()
        if button is not None and isinstance(button, QPushButton):
            print("Button clicked:", button.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChatWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        self.history_box = QScrollArea()
        history_widget = QWidget()
        history_layout = QGridLayout()
        history_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        for i in range(50):
            label = QLabel()
            label.setText(f'Conversation {i + 1}')
            label.setStyleSheet('background-color: cyan')
            if i % 2 == 0:
                label.setAlignment(Qt.AlignRight)
            history_layout.addWidget(label, i, i % 2, 1, 2)
            history_layout.setRowMinimumHeight(i,40)
        history_widget.setLayout(history_layout)
        self.history_box.setWidget(history_widget)
        self.question_box = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.history_box)
        layout.addWidget(self.question_box)
        self.setLayout(layout)
    
    def get_answer(self):
        return 'Proper answer from ChatPDF'

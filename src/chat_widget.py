from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChatWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.history_box = QScrollArea()
        self.history_box.setWidgetResizable(True)
        self.history_box.setFocusPolicy(Qt.NoFocus)
        self.history_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.question_box = QLineEdit()

        space = 30
        margin = 5
        
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(margin, margin, margin, margin)
        for i in range(50):
            dialogue = QLabel()
            dialogue.setWordWrap(True)
            dialogue.setText(' '.join(['Some Text' for _ in range(i + 1)]))
            self.history_box.setMinimumWidth(space + 2 * margin +  dialogue.minimumSizeHint().width() + self.history_box.verticalScrollBar().sizeHint().width() + 2 * self.history_box.frameWidth())
            dialogue_layout = QHBoxLayout()
            if i % 2 == 0:
                dialogue.setStyleSheet('background-color: cyan')
                dialogue_layout.addWidget(dialogue)
                dialogue_layout.addStretch(1)
                dialogue_layout.addSpacing(30)
            else:
                dialogue.setStyleSheet('background-color: yellow')
                dialogue_layout.addSpacing(30)
                dialogue_layout.addStretch(1)
                dialogue_layout.addWidget(dialogue)
            history_layout.addLayout(dialogue_layout)

        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(history_layout)
        self.history_box.setWidget(widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.history_box)
        layout.addWidget(self.question_box)
        self.setLayout(layout)

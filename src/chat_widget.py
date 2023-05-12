from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ChatWidget(QWidget):
    requested = pyqtSignal(str)
    chatbotRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initial_state = False
        self.min_width = 0
        self.space = 30
        self.margin = 5
        self.answer_color = 'cyan'
        self.question_color = 'yellow'
        self.setLayout(QVBoxLayout())
        self.init_initial_ui()
        self.setMinimumWidth(self.min_width)
    
    def init_initial_ui(self):
        if self.initial_state:
            return
        
        deleteItemsOfLayout(self.layout())  
        self.initial_state = True

        chatbot_button = QPushButton()
        chatbot_button.setText('Load Chatbot')
        chatbot_button.clicked.connect(self.load_chatbot)
        self.layout().addWidget(chatbot_button)

    def init_chatbot_ui(self):
        deleteItemsOfLayout(self.layout())  
        self.initial_state = False

        self.history_box = QScrollArea()
        self.history_box.setWidgetResizable(True)
        self.history_box.setFocusPolicy(Qt.NoFocus)
        self.history_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.question_box = QLineEdit()
        self.question_box.returnPressed.connect(self.push_question)
        
        self.history_layout = QVBoxLayout()
        self.history_layout.addStretch(1)
        self.history_layout.setContentsMargins(*([self.margin] * 4))

        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.history_layout)
        self.history_box.setWidget(widget)

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.history_box)
        self.layout().addWidget(self.question_box)
    
    def load_chatbot(self):
        self.init_chatbot_ui()
        self.chatbotRequested.emit()
    
    def push_question(self):
        self.question_box.clearFocus()
        question = self.question_box.text()
        self.question_box.clear()
        self.push_dialogue(question, is_answer=False)
        self.requested.emit(question)
    
    def push_answer(self, answer):
        self.push_dialogue(answer)
    
    def push_dialogue(self, text, is_answer=True):
        dialogue = QLabel()
        dialogue.setWordWrap(True)
        dialogue.setText(text)

        color = self.answer_color if is_answer else self.question_color
        dialogue.setStyleSheet(f'background-color: {color}')
        # dialogue.setMaximumHeight(dialogue.sizeHint().height())

        if self.min_width < dialogue.minimumSizeHint().width():
            self.min_width = dialogue.minimumSizeHint().width()
            self.history_box.setMinimumWidth(self.space + 2 * self.margin + self.min_width + 
                                             self.history_box.verticalScrollBar().sizeHint().width() + 
                                             2 * self.history_box.frameWidth())

        layout = QHBoxLayout()
        if is_answer:
            layout.addWidget(dialogue)
            layout.addStretch(1)
            layout.addSpacing(self.space)
        else:
            layout.addSpacing(self.space)
            layout.addStretch(1)
            layout.addWidget(dialogue)
        self.history_layout.addLayout(layout)
    

def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

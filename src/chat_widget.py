from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChatWidget(QWidget):
    requested = pyqtSignal(str, bool, str)
    chatbotRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initial_state = False
        self.answered = True
        self.addl_q = False
        self.language = 'ko'
        self.min_width = 0
        self.space = 30
        self.margin = 5
        self.answer_color = 'cyan'
        self.question_color = 'yellow'
        self.question_box = None

        self.setLayout(QVBoxLayout())
        self.setMinimumWidth(self.min_width)

    def init_initial_ui(self):
        if self.initial_state:
            return
        deleteItemsOfLayout(self.layout())
        self.initial_state = True

        chatbot_button = QPushButton()
        chatbot_button.setFocusPolicy(Qt.NoFocus)
        chatbot_button.setText('Load Chatbot')
        chatbot_button.clicked.connect(self.load_chatbot)
        self.layout().addWidget(chatbot_button)

    def init_loading_ui(self):
        deleteItemsOfLayout(self.layout())
        self.initial_state = False

        loading_message = QLabel()
        loading_message.setText('Now Loading...')
        loading_message.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(loading_message)

    def init_chatbot_ui(self):
        deleteItemsOfLayout(self.layout())
        self.initial_state = False

        addl_q_box = QCheckBox('Create Additional Question')
        addl_q_box.stateChanged.connect(self.addl_q_setting_changed)

        language_label = QLabel('Language : ')
        lang_sel_box = QComboBox()
        lang_sel_box.addItems(['ko', 'en', 'ja', 'zh-CN'])
        lang_sel_box.setFocusPolicy(Qt.ClickFocus)
        lang_sel_box.currentIndexChanged.connect(self.lang_changed)
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(language_label)
        lang_layout.addWidget(lang_sel_box)
        lang_widget = QWidget()
        lang_widget.setLayout(lang_layout)

        self.history_box = QScrollArea()
        self.history_box.setWidgetResizable(True)
        self.history_box.setFocusPolicy(Qt.NoFocus)
        self.history_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.history_box.verticalScrollBar().rangeChanged.connect(
            lambda: self.history_box.verticalScrollBar().setValue(self.history_box.verticalScrollBar().maximum()))
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
        self.layout().addWidget(addl_q_box)
        self.layout().addWidget(lang_widget)
        self.layout().addWidget(self.history_box)
        self.layout().addWidget(self.question_box)

    def load_chatbot(self):
        self.init_loading_ui()
        self.chatbotRequested.emit()

    def push_question(self):
        if not self.answered:
            return

        self.answered = False
        self.question_box.clearFocus()
        question = self.question_box.text()

        self.question_box.clear()
        self.push_dialogue(question, is_answer=False)
        self.requested.emit(question, self.addl_q, self.language)

    def push_answer(self, answer):
        self.answered = True
        self.push_dialogue(answer)

    def push_dialogue(self, text, is_answer=True):
        dialogue = QLabel()
        dialogue.setWordWrap(True)
        dialogue.setText(text)

        color = self.answer_color if is_answer else self.question_color
        dialogue.setStyleSheet(f'background-color: {color}')

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
    
    def addl_q_setting_changed(self, state):
        if state == 2:
            self.addl_q = True
        else:
            self.addl_q = False
    
    def lang_changed(self):
        self.language = self.sender().currentText()


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

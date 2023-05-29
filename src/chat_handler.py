class ChatHandler:
    def __init__(self, chat_widget):
        self.chat_widget = chat_widget
        self.initial_state = False
        self.answered = True
        self.addl_q = False
        self.language = 'ko'
    
    def init_initial_ui(self):
        if self.initial_state:
            return
        
        self.initial_state = True
        self.chat_widget.init_initial_ui()
    
    def init_loading_ui(self):
        self.initial_state = False
        self.chat_widget.init_loading_ui()
    
    def init_chatbot_ui(self):
        self.initial_state = False
        self.chat_widget.init_chatbot_ui()
    
    def load_chatbot(self):
        self.init_loading_ui()
        self.chat_widget.chatbotRequested.emit()
    
    def push_question(self):
        if not self.answered:
            return

        self.answered = True
        question = self.chat_widget.get_question()
        self.chat_widget.push_dialogue(question, is_answer=False)
        self.chat_widget.requested.emit(question, self.addl_q, self.language)

    def push_answer(self, result):
        self.answered = True
        if self.addl_q:
            self.chat_widget.set_addl_q(result[1:])
        self.chat_widget.push_dialogue(result[0])        

    def addl_q_requested(self, question):
        print(question)
        if not self.answered:
            return

        if question:
            self.answered = False
            self.chat_widget.push_dialogue(question, is_answer=False)
            self.chat_widget.requested.emit(question, self.addl_q, self.language)
    
    def set_addl_q_setting(self, state):
        if not self.answered:
            return
    
        if state == 2:
            self.addl_q = True
            self.chat_widget.create_addl_q_boxes()
        else:
            self.addl_q = False
            self.chat_widget.destroy_addl_q_boxes()
    
    def set_language(self, language):
        self.language = language
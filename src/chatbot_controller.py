class ChatbotController:
    def __init__(self, pdf, push_answer):
        self.pdf = pdf
        self.push_answer = push_answer

    def handle_request(self, question):
        query = question
        answer = ' '.join(['proper answer' for _ in range(10)])
        self.push_answer(answer)

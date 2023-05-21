import os
from PyQt5.QtCore import QThread, pyqtSignal
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from transformers import GPT2TokenizerFast
from dotenv import load_dotenv


class ChatbotController:
    def __init__(self, pdf, chat_widget):
        self.pdf = pdf
        self.chat_widget = chat_widget
        self.question = ''
        self.chat_history = []

        self.init_chatbot_thread = InitChatbotThread(self)
        self.init_chatbot_thread.finished.connect(
            self.chat_widget.init_chatbot_ui)
        self.init_chatbot_thread.start()

        self.handle_request_thread = HandleRequestThread(self)
        self.handle_request_thread.finished.connect(
            self.chat_widget.push_answer)

    def handle_request(self, question):
        self.question = question
        self.handle_request_thread.start()


class InitChatbotThread(QThread):
    finished = pyqtSignal()

    def __init__(self, chatbot_controller):
        super().__init__()
        self.controller = chatbot_controller

    def run(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.environ.get('API_KEY')

        text = ''
        for page in self.controller.pdf:
            text += page.get_text(sort=True) + '\n'

        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=24,
            length_function=lambda x: len(tokenizer.encode(x)),
        )
        chunks = text_splitter.create_documents([text])
        embeddings = OpenAIEmbeddings()

        db = FAISS.from_documents(chunks, embeddings)
        self.controller.chat_bot = ConversationalRetrievalChain.from_llm(
            OpenAI(temperature=0.1), db.as_retriever())
        self.finished.emit()


class HandleRequestThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, chatbot_controller):
        super().__init__()
        self.controller = chatbot_controller

    def run(self):
        result = self.controller.chat_bot(
            {"question": self.controller.question, "chat_history": self.controller.chat_history})
        self.controller.chat_history.append(
            (self.controller.question, result['answer']))
        self.finished.emit(result['answer'])

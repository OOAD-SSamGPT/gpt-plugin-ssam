import os
from PyQt5.QtCore import QThread, pyqtSignal
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader

# for papago
import json
import urllib.request
load_dotenv()


class ChatbotController:
    def __init__(self, file_path, chat_widget):
        self.file_path = file_path
        self.chat_widget = chat_widget
        self.question = ''
        self.addl_q = False
        self.language = 'ko'
        self.chat_history = []

        self.init_chatbot_thread = InitChatbotThread(self)
        self.init_chatbot_thread.finished.connect(
            self.chat_widget.init_chatbot_ui)
        self.init_chatbot_thread.start()

        self.handle_request_thread = HandleRequestThread(self)
        self.handle_request_thread.finished.connect(
            self.chat_widget.push_answer)

    def handle_request(self, question, addl_q, language):
        self.question = question
        self.addl_q = addl_q
        self.language = language
        self.handle_request_thread.start()


class InitChatbotThread(QThread):
    finished = pyqtSignal()

    def __init__(self, chatbot_controller):
        super().__init__()
        self.controller = chatbot_controller

    def run(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.environ.get('API_KEY')

        loader = PyPDFLoader(self.controller.file_path)
        chunks = loader.load_and_split()
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

        self.controller.question = self.translate(
            self.controller.question, self.controller.language, "en")
        result = self.controller.chat_bot(
            {"question": self.controller.question, "chat_history": self.controller.chat_history})
        result = self.translate(
            result['answer'], "en", self.controller.language)

        self.controller.chat_history.append(
            (self.controller.question, result))
        # result = f"proper answer with\nadditional_question : {self.controller.addl_q}\nlanguage : {self.controller.language}"
        self.finished.emit(result)

    def translate(self, question, src, tar) -> str:
        if src == 'en' and tar == 'en':
            return question
        # 개발자센터에서 발급받은 Client ID 값
        client_id = os.environ.get('PAPAGO_CLIENT')
        # 개발자센터에서 발급받은 Client Secret 값
        client_secret = os.environ.get('PAPAGO_SECRET')

        encText = urllib.parse.quote(question)
        data = f"source={src}&target={tar}&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))

        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            json_data = json.loads(response_body.decode('utf-8'))
            result = json_data['message']['result']['translatedText']
        else:
            result = f"Error Code : {rescode}"
        return result

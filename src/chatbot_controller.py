import os
from PyQt5.QtCore import QThread, pyqtSignal
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from transformers import GPT2TokenizerFast
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader

import textract

# for papago
import sys
import json
import urllib.request


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

        loader = PyPDFLoader("./assets/test.pdf")
        pages = loader.load_and_split()
        chunks = pages
        # doc = textract.process("./assets/test.pdf")
        # with open('test.txt', 'w') as f:
        #     f.write(doc.decode('utf-8'))

        # with open('test.txt', 'r') as f:
        #     text = f.read()

        # for i in pages:
        #     print(i)
        # # text = ''
        # # for page in self.controller.pdf:
        # #     text += page.get_text(sort=True) + '\n'

        # # Step 2: Save to .txt and reopen (helps prevent issues)

        # tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=512,
        #     chunk_overlap=24,
        #     length_function=lambda x: len(tokenizer.encode(x)),
        # )
        # chunks = text_splitter.create_documents([text])
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
            self.controller.question, "ko", "en")
        result = self.controller.chat_bot(
            {"question": self.controller.question, "chat_history": self.controller.chat_history})
        print(result)
        result = self.translate(result['answer'], "en", "ko")
        print(result)
        self.controller.chat_history.append(
            (self.controller.question, result))
        self.finished.emit(result)

    def translate(self, question, src, tar) -> str:
        client_id = "5EnH0B4Nm1uSYVsKPt4v"  # 개발자센터에서 발급받은 Client ID 값
        client_secret = "xXeIiZl829"  # 개발자센터에서 발급받은 Client Secret 값
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
            print(json_data['message']['result']['translatedText'])
        else:
            print("Error Code:" + rescode)

        return json_data['message']['result']['translatedText']

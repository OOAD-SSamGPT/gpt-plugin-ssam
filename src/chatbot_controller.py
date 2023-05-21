import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from transformers import GPT2TokenizerFast
from dotenv import load_dotenv

class ChatbotController:
    def __init__(self, pdf, push_answer):
        self.pdf = pdf
        self.push_answer = push_answer
        self.chat_history = []
        self.init_chatbot()
    
    def init_chatbot(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.environ.get('API_KEY')

        text = ''
        for page in self.pdf:
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
        self.chat_bot = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), db.as_retriever())

    def handle_request(self, question):
        result = self.chat_bot({"question": question, "chat_history": self.chat_history})
        self.chat_history.append((question, result['answer']))
        self.push_answer(result['answer'])

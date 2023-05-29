import fitz
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

from chatbot_controller import ChatbotController
from chat_handler import ChatHandler


class MainController:
    def __init__(self, window, widgets, actions):
        self.pdf = None
        self.idx = 0
        self.max_idx = 0
        self.file_path = ''
        self.window = window

        self.pageview_widget = widgets['pageview']
        self.note_widget = widgets['note']
        self.chat_widget = widgets['chat']
        self.preview_widget = widgets['preview']
        self.idx_widget = widgets['idx']
        self.scale_widget = widgets['scale']

        self.open_action = actions['open']
        self.save_action = actions['save']

        self.chat_handler = ChatHandler(self.chat_widget)
        self.chat_widget.set_handler(self.chat_handler)

        self.connect_events()
    
    def connect_events(self):
        self.pageview_widget.resized.connect(self.page_resized)
        self.chat_widget.chatbotRequested.connect(self.load_chatbot)
        self.preview_widget.idxChanged.connect(self.idx_changed)
        self.idx_widget.idxChanged.connect(self.idx_changed)
        self.scale_widget.scaleChanged.connect(self.scale_changed)

        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
    
    def page_resized(self, scale):
        self.scale_widget.set_scale(scale)

    def load_chatbot(self):
        if self.pdf:
            self.chatbot_controller = ChatbotController(
                self.file_path, self.chat_handler)
            self.chat_widget.requested.connect(
                self.chatbot_controller.handle_request)
    
    def idx_changed(self, idx):
        if self.pdf:
            self.idx = idx
            self.pageview_widget.set_page(self.pdf[idx])
            self.preview_widget.set_idx(idx)
            self.idx_widget.set_idx(idx)
            self.note_widget.set_idx(idx)
    
    def scale_changed(self, scale, scale_policy):
        scale = self.pageview_widget.set_scale(scale, scale_policy)
        self.scale_widget.set_scale(scale)
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window, 'Open file', '', 'PDF Files (*.pdf)')
        if not file_path:
            return
        
        self.file_path = file_path
        self.pdf = fitz.open(file_path)
        self.idx = 0
        self.max_idx = self.pdf.page_count - 1

        self.idx_widget.set_idx(self.idx)
        self.idx_widget.set_max_idx(self.max_idx)
        self.preview_widget.set_pdf(self.pdf)
        self.pageview_widget.set_page(self.pdf[0])
        self.note_widget.load_notes(self.pdf)
        self.chat_handler.init_initial_ui()
    
    def save_file(self):
        if self.pdf:
            self.note_widget.save_note()
            self.pdf.save(self.pdf.name, incremental=True,
                          encryption=fitz.PDF_ENCRYPT_KEEP)
    
    def key_pressed(self, key):
        if self.pdf:
            if key == Qt.Key_Right and self.idx < self.max_idx:
                self.idx_changed(self.idx + 1)
            elif key == Qt.Key_Left and self.idx > 0:
                self.idx_changed(self.idx - 1)
    
    def mouse_pressed(self, button, sender):
        if self.pdf and button == Qt.LeftButton:
            if sender != self.note_widget:
                self.note_widget.update_note()
            if sender != self.chat_widget.question_box:
                self.chat_widget.question_box.clearFocus()
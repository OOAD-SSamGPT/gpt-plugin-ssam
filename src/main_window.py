import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import fitz


from pageview_widget import PageviewWidget
from preview_widget import PreviewWidget
from idx_widget import IdxWidget
from scale_widget import ScaleWidget
from note_widget import NoteWidget
from chat_widget import ChatWidget
from chatbot_controller import ChatbotController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.pdf = None
        self.idx = 0
        self.max_idx = 0
        self.init_ui()
        self.show()

    def init_ui(self):
        self.resize(1000, 800)
        self.setWindowTitle('PDF Viewer')

        self.pageview_widget = PageviewWidget()
        self.pageview_widget.resized.connect(self.page_resized)
        self.note_widget = NoteWidget()
        self.chat_widget = ChatWidget()
        self.chat_widget.chatbotRequested.connect(self.load_chatbot)
        self.preview_widget = PreviewWidget()
        self.preview_widget.idxChanged.connect(self.idx_changed)
        self.idx_widget = IdxWidget()
        self.idx_widget.idxChanged.connect(self.idx_changed)
        self.scale_widget = ScaleWidget()
        self.scale_widget.scaleChanged.connect(self.scale_changed)

        self.init_menu_bar()
        self.init_tool_bar()

        self.sub_splitter = QSplitter()
        self.sub_splitter.setOrientation(Qt.Orientation.Vertical)
        self.sub_splitter.addWidget(self.pageview_widget)
        self.sub_splitter.addWidget(self.note_widget)
        self.sub_splitter.setSizes([1000, 100])

        self.main_splitter = QSplitter()
        self.main_splitter.addWidget(self.preview_widget)
        self.main_splitter.addWidget(self.sub_splitter)
        self.main_splitter.addWidget(self.chat_widget)
        self.main_splitter.setSizes([100, 1000, 300])

        layout = QHBoxLayout()
        layout.addWidget(self.main_splitter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def init_menu_bar(self):
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('File')
        filemenu.addAction(open_action)
        filemenu.addAction(save_action)

    def init_tool_bar(self):
        idx_action = QWidgetAction(self)
        idx_action.setDefaultWidget(self.idx_widget)

        scale_action = QWidgetAction(self)
        scale_action.setDefaultWidget(self.scale_widget)

        tool_bar = QToolBar(self)
        tool_bar.addAction(idx_action)
        tool_bar.addAction(scale_action)
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)
        self.addToolBar(tool_bar)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window(), 'Open file', '', 'PDF Files (*.pdf)')
        self.pdf = fitz.open(file_path)
        self.idx = 0
        self.max_idx = self.pdf.page_count - 1
        self.idx_widget.set_idx(self.idx)
        self.idx_widget.set_max_idx(self.max_idx)
        self.preview_widget.set_pdf(self.pdf)
        self.pageview_widget.set_page(self.pdf[0])
        self.note_widget.load_notes(self.pdf)
        self.chat_widget.init_initial_ui()

    def save_file(self):
        if self.pdf:
            self.note_widget.save_note()
            self.pdf.save(self.pdf.name, incremental=True,
                          encryption=fitz.PDF_ENCRYPT_KEEP)

    # main events
    def keyPressEvent(self, event):
        if self.pdf:
            if event.key() == Qt.Key_Right and self.idx < self.max_idx:
                self.idx_changed(self.idx + 1)
            elif event.key() == Qt.Key_Left and self.idx > 0:
                self.idx_changed(self.idx - 1)

    def mousePressEvent(self, event):
        if self.pdf and event.button() == Qt.LeftButton:
            if self.sender() != self.note_widget:
                self.note_widget.update_note()
            if self.sender() != self.chat_widget.question_box:
                self.chat_widget.question_box.clearFocus()

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

    def page_resized(self, scale):
        self.scale_widget.set_scale(scale)

    def load_chatbot(self):
        if self.pdf:
            self.chatbot_controler = ChatbotController(
                self.pdf, self.chat_widget)
            self.chat_widget.requested.connect(
                self.chatbot_controler.handle_request)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

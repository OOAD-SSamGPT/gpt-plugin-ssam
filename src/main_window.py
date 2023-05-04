import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import fitz

from pageview_widget import PageviewWidget
from preview_widget import PreviewWidget
from idx_widget import IdxWidget
from scale_widget import ScaleWidget


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.pdf = None
        self.idx = 0
        self.max_idx = 0
        self.scale = 1
        self.init_ui()
        self.show()
    
    def init_ui(self):
        self.resize(1000, 800)
        self.setWindowTitle('PDF Viewer')

        self.pageview_widget = PageviewWidget()
        self.preview_widget = PreviewWidget()
        self.preview_widget.idxChanged.connect(self.idx_changed)
        self.idx_widget = IdxWidget()
        self.idx_widget.idxChanged.connect(self.idx_changed)
        self.scale_widget = ScaleWidget()
        self.scale_widget.scaleChanged.connect(self.scale_changed)

        self.init_menu_bar()
        self.init_tool_bar()

        splitter = QSplitter()
        splitter.addWidget(self.preview_widget)
        splitter.addWidget(self.pageview_widget)
        
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def init_menu_bar(self):
        file_menu = QMenu('File', self)
        self.menuBar().addMenu(file_menu)
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
    
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
    
    # events for menu bar
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window(), 'Open file', '', 'PDF Files (*.pdf)')
        self.pdf = fitz.open(file_path)
        self.max_idx = len(self.pdf) - 1
        self.idx = 0
        self.idx_widget.set_idx(self.idx)
        self.idx_widget.set_max_idx(self.max_idx)
        self.preview_widget.set_pdf(self.pdf)
        self.pageview_widget.set_page(self.pdf[0])

    # main events
    def keyPressEvent(self, event):
        if self.pdf:
            if event.key() == Qt.Key_Right and self.idx < self.max_idx:
                self.idx_changed(self.idx + 1)
            elif event.key() == Qt.Key_Left and self.idx > 0:
                self.idx_changed(self.idx - 1)
    
    def idx_changed(self, idx):
        if self.pdf and self.idx != idx:
            self.idx = idx
            self.pageview_widget.set_page(self.pdf[idx])
            self.preview_widget.set_idx(idx)
            self.idx_widget.set_idx(idx)
    
    def scale_changed(self, scale):
        if self.pdf and self.scale != scale:
            self.scale = round(scale, 4)
            self.pageview_widget.set_scale(self.scale)
            self.scale_widget.set_scale(self.scale)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
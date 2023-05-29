import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


from pageview_widget import PageviewWidget
from preview_widget import PreviewWidget
from idx_widget import IdxWidget
from scale_widget import ScaleWidget
from note_widget import NoteWidget
from chat_widget import ChatWidget
from event_handler import EventHandler


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.resize(1000, 800)
        self.setWindowTitle('PDF Viewer')

        self.pageview_widget = PageviewWidget()
        self.note_widget = NoteWidget()
        self.chat_widget = ChatWidget()
        self.preview_widget = PreviewWidget()
        self.idx_widget = IdxWidget()
        self.scale_widget = ScaleWidget()

        widgets = {}
        widgets['pageview'] = self.pageview_widget
        widgets['note'] = self.note_widget
        widgets['chat'] = self.chat_widget
        widgets['preview'] = self.preview_widget
        widgets['idx'] = self.idx_widget
        widgets['scale'] = self.scale_widget

        actions = self.init_menu_bar()
        self.event_handler = EventHandler(self.window(), widgets, actions)

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
        save_action = QAction('Save', self)

        actions = {}
        actions['open'] = open_action
        actions['save'] = save_action

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('File')
        filemenu.addAction(open_action)
        filemenu.addAction(save_action)
        return actions

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

    # main events
    def keyPressEvent(self, event):
        self.event_handler.key_pressed(event.key())

    def mousePressEvent(self, event):
        self.event_handler.mouse_pressed(event.button(), self.sender())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QMenu, QAction, QFileDialog, QToolBar, QWidgetAction, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz

class PdfViewer(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.pdf = None
        self.page_num = 0
        self.max_page_num = 0
        self.scale = 1
        self.init_ui()
        self.show()
    
    def init_ui(self):
        self.resize(500, 400)
        self.setWindowTitle('PDF Viewer')

        self.init_page_screen()
        self.init_menu_bar()
        self.init_tool_bar()
    
    def init_page_screen(self):
        self.page_screen = QLabel()
        layout = QHBoxLayout()
        layout.addWidget(self.page_screen)
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
        self.page_num_box = QLineEdit('1', self)
        self.page_num_box.setFixedWidth(60)
        self.page_num_box.setAlignment(Qt.AlignCenter)
        self.page_num_box.setFocusPolicy(Qt.ClickFocus)
        self.page_num_box.editingFinished.connect(self.page_num_changed)
        self.max_page_num_label = QLabel('/ 1', self)
        self.max_page_num_label.setAlignment(Qt.AlignCenter)
        next_button = QPushButton('>', self)
        next_button.setFocusPolicy(Qt.NoFocus)
        next_button.setFixedWidth(30)
        next_button.clicked.connect(self.next_button_clicked)
        previous_button = QPushButton('<', self)
        previous_button.setFocusPolicy(Qt.NoFocus)
        previous_button.setFixedWidth(30)
        previous_button.clicked.connect(self.previous_button_clicked)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(previous_button)
        layout.addSpacing(20)
        layout.addWidget(self.page_num_box)
        layout.addWidget(self.max_page_num_label)
        layout.addSpacing(20)
        layout.addWidget(next_button)
        layout.addStretch(1)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(widget)

        tool_bar = QToolBar(self)
        tool_bar.addAction(widget_action)
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)
        self.addToolBar(tool_bar)
    
    # events for menu bar
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window(), 'Open file', '', 'PDF Files (*.pdf)')
        self.pdf = fitz.open(file_path)
        self.max_page_num = len(self.pdf) - 1
        self.max_page_num_label.setText('/ ' + str(len(self.pdf)))
        self.draw_page()
    
    # events for tool bar
    def previous_button_clicked(self):
        if self.pdf and self.page_num > 0:
            self.page_num -= 1
            self.page_num_box.setText(str(self.page_num + 1))
            self.draw_page()
    
    def next_button_clicked(self):
        if self.pdf and self.page_num < self.max_page_num:
            self.page_num += 1
            self.page_num_box.setText(str(self.page_num + 1))
            self.draw_page()
    
    def page_num_changed(self):
        if self.pdf:
            try:
                goal = int(self.page_num_box.text()) - 1
                if goal < 0:
                    self.page_num_box.setText('1')
                    self.page_num = 0
                elif self.max_page_num < goal:
                    self.page_num_box.setText(str(self.max_page_num + 1))
                    self.page_num = self.max_page_num
                else:
                    self.page_num = goal
                self.draw_page()
            except:
                self.page_num_box.setText(str(self.page_num + 1))
        else:
            self.page_num_box.setText('1')
        self.page_num_box.clearFocus()

    # main events
    def keyPressEvent(self, event):
        if self.pdf:
            if event.key() == Qt.Key_Right and self.page_num < self.max_page_num:
                self.page_num += 1
                self.page_num_box.setText(str(self.page_num + 1))
                self.draw_page()
            elif event.key() == Qt.Key_Left and self.page_num > 0:
                self.page_num -= 1
                self.page_num_box.setText(str(self.page_num + 1))
                self.draw_page()
    
    # methods
    def draw_page(self):
        page = self.pdf[self.page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
        qimage = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.page_screen.setPixmap(pixmap)
        self.page_screen.resize(pixmap.width(), pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfViewer()
    sys.exit(app.exec_())

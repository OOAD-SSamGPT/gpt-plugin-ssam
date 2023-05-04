import fitz
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PageviewWidget(QScrollArea):
    
    def __init__(self):
        super().__init__()
        self.page = None
        self.scale = 1
        self.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)


        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.label)
    
    def set_page(self, page):
        self.page = page
        self.draw_page()
    
    def set_scale(self, scale):
        self.scale = scale
        self.draw_page()
    
    def draw_page(self):
        if not self.page:
            return

        # x_scale = self.width() / self.page.rect.width
        # y_scale = self.height() / self.page.rect.height
        
        # scale = min(x_scale, y_scale)
        print(self.scale)
        pix = self.page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
        qimage = QImage(pix.samples_ptr, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())
    
    def resizeEvent(self, event):
        self.draw_page()
    
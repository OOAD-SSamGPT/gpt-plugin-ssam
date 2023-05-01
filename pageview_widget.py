import fitz
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PageviewWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.page = None
    
    def set_page(self, page):
        self.page = page
        self.draw_page()
    
    def draw_page(self):
        if not self.page:
            return

        x_scale = self.width() / self.page.rect.width
        y_scale = self.height() / self.page.rect.height
        
        scale = min(x_scale, y_scale)
        pix = self.page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        qimage = QImage(pix.samples_ptr, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(pixmap)
    
    def resizeEvent(self, event):
        self.draw_page()
    

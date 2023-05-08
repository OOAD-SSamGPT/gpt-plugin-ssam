import fitz
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PageviewWidget(QScrollArea):
    resized = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.page = None
        self.scale = 1
        self.scale_policy = '사용자 설정'
        self.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.label)
    
    def set_page(self, page):
        self.page = page
        self.draw_page()
    
    def set_scale(self, scale, scale_policy):
        self.scale = scale
        self.scale_policy = scale_policy
        self.draw_page()
        return self.scale
    
    def draw_page(self):
        if not self.page:
            return

        if self.scale_policy == '사용자 설정':
            pass
        elif self.scale_policy == '페이지 맞춤':
            x_scale = (self.width() - 2 * self.frameWidth() - self.verticalScrollBar().width()) / self.page.rect.width
            y_scale = (self.height() - 2 * self.frameWidth()) / self.page.rect.height
            self.scale = min(x_scale, y_scale)
        elif self.scale_policy == '너비 맞춤':
            self.scale = (self.width() - 2 * self.frameWidth() - self.verticalScrollBar().width()) / self.page.rect.width
        
        pix = self.page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale), annots=True)
        qimage = QImage(pix.samples_ptr, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
    
    def resizeEvent(self, event):
        self.draw_page()
        self.resized.emit(self.scale)
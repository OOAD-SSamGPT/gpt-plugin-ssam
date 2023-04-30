import fitz
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PreviewScreen(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalScrollBar().setEnabled(False)
    
    def draw_preview(self, pdf):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        for i in range(len(pdf)):
            page = pdf[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
            qimage = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)
        self.setWidget(widget)
        self.setFixedWidth(widget.sizeHint().width() + 2 * self.frameWidth() + \
                           self.verticalScrollBar().sizeHint().width())

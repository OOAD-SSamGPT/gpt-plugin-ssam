import fitz
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PreviewItem(QWidget):

    def __init__(self, idx, page):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        pix = page.get_pixmap(matrix=fitz.Matrix(0.15, 0.15))
        qimage = QImage(pix.samples_ptr, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        idx_label = QLabel(str(idx + 1))
        idx_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(idx_label)
        self.setStyleSheet("background-color: orange;")

        self.resize(self.minimumWidth() + 5, self.minimumHeight() + 5)


class PreviewWidget(QScrollArea):

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalScrollBar().setEnabled(False)
        self.preview_items = []
    
    def draw_preview(self, pdf):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        for i, page in enumerate(pdf):
            preview_item = PreviewItem(i, page)
            layout.addWidget(preview_item)
            self.preview_items.append(preview_item)
        
        self.setWidget(widget)
        self.setFixedWidth(widget.sizeHint().width() + 2 * self.frameWidth() + \
                           self.verticalScrollBar().sizeHint().width())
    
        self.preview_items[3].setStyleSheet("background-color: red;")
        self.preview_items[2].setStyleSheet("background-color: orange;")

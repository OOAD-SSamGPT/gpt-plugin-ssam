from PyQt5 import QtGui
import fitz
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PreviewItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, idx, page):
        super().__init__()
        self.idx = idx
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()

        layout.setSpacing(0)

        pix = page.get_pixmap(matrix=fitz.Matrix(0.15, 0.15), annots=False)
        qimage = QImage(pix.samples_ptr, pix.width, pix.height,
                        pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        idx_label = QLabel(str(idx + 1))
        idx_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(idx_label)
        self.setLayout(layout)

    def mouseReleaseEvent(self, event):
        self.clicked.emit(self.idx)


class PreviewFactory:
    def create(self, pdf, callback, layout):
        preview_items = []
        for i, page in enumerate(pdf):
            preview_item = PreviewItem(i, page)
            preview_item.clicked.connect(callback)
            layout.addWidget(preview_item)
            preview_items.append(preview_item)
        return preview_items


class PreviewWidget(QScrollArea):
    idxChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.idx = 0
        self.preview_items = []

        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalScrollBar().setEnabled(False)

    def set_pdf(self, pdf):
        self.idx = 0
        for preview_item in self.preview_items:
            preview_item.setParent(None)
        self.preview_items = []

        widget = QWidget()
        widget.setStyleSheet('background-color: white;')
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.preview_items = PreviewFactory().create(pdf, self.preview_item_clicked, layout)
        
        self.setWidget(widget)
        self.setFixedWidth(self.sizeHint().width() + 2 * self.frameWidth() +
                           self.verticalScrollBar().sizeHint().width())
        self.preview_items[0].setStyleSheet('background-color: orange;')

    def set_idx(self, idx):
        self.preview_items[self.idx].setStyleSheet('background-color: white;')
        self.preview_items[idx].setStyleSheet('background-color: orange;')
        self.idx = idx
        self.ensureWidgetVisible(self.preview_items[self.idx], yMargin=0)

    def preview_item_clicked(self, idx):
        self.idxChanged.emit(idx)

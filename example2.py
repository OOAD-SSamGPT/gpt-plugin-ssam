from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
import fitz

app = QApplication([])
window = QWidget()
layout = QVBoxLayout(window)
scroll_area = QScrollArea()
pdf = fitz.open('test.pdf')

for i in range(len(pdf)):
    page = pdf[i]
    pix = page.get_pixmap()
    qimage = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    label = QLabel()
    label.setPixmap(pixmap)
    layout.addWidget(label)

scroll_area.setWidgetResizable(True)
scroll_area.setWidget(window)
scroll_area.show()
app.exec_()

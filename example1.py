import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.page_num = 0
        self.pdf = fitz.open('test.pdf')
        self.matrix = fitz.Matrix(1.3, 1.3)
        self.draw_page()
        self.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.page_num += 1
        elif event.key() == Qt.Key_Left:
            self.page_num -= 1
        self.page_num %= len(self.pdf)
        self.draw_page()

    def draw_page(self):
        page = self.pdf[self.page_num]
        pix = page.get_pixmap(matrix=self.matrix)
        qimage = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.setWindowTitle(f'{self.page_num}')

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

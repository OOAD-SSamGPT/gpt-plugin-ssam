from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtPrintSupport import QPdfDocument, QPdfView

app = QApplication([])
window = QMainWindow()
pdf_doc = QPdfDocument()
pdf_doc.load('./HW_2/20191579_객체지향분석및설계_HW2.pdf')
pdf_view = QPdfView(pdf_doc)
pdf_view.setRenderHint(QPainter.Antialiasing, True)
window.setCentralWidget(pdf_view)
window.show()
app.exec_()

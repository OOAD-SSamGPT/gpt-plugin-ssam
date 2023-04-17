from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication([])
view = QWebEngineView()
view.load(QUrl.fromLocalFile('./HW_2/20191579_객체지향분석및설계_HW2.pdf'))
view.show()
app.exec()

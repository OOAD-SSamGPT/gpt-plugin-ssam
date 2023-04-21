import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit, QToolBar, QAction, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 위젯 생성
        self.list_widget = QListWidget()
        self.text_edit = QTextEdit()
        self.splitter = QSplitter()
        self.splitter.addWidget(self.list_widget)
        self.splitter.addWidget(self.text_edit)
        self.setCentralWidget(self.splitter)

        # 툴바 추가
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # 버튼 추가
        self.action = QAction("Add new widget", self)
        self.action.triggered.connect(self.add_new_widget)
        self.toolbar.addAction(self.action)

    def add_new_widget(self):
        # 새로운 위젯 생성
        new_widget = QWidget()
        layout = QVBoxLayout(new_widget)
        layout.addWidget(QLineEdit())
        layout.addWidget(QPushButton("Do something"))
        self.splitter.insertWidget(0, new_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

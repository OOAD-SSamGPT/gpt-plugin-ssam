from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal


class IdxWidget(QWidget):
    idxChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.max_idx = 0
        self.idx = 0

        self.idx_box = QLineEdit('1', self)
        self.idx_box.setFixedWidth(60)
        self.idx_box.setAlignment(Qt.AlignCenter)
        self.idx_box.setFocusPolicy(Qt.ClickFocus)
        self.idx_box.editingFinished.connect(self.idx_editing_finished)

        self.max_idx_label = QLabel('/ 1', self)
        self.max_idx_label.setAlignment(Qt.AlignCenter)

        next_button = QPushButton('>', self)
        next_button.setFocusPolicy(Qt.NoFocus)
        next_button.setFixedWidth(30)
        next_button.clicked.connect(self.next_button_clicked)

        previous_button = QPushButton('<', self)
        previous_button.setFocusPolicy(Qt.NoFocus)
        previous_button.setFixedWidth(30)
        previous_button.clicked.connect(self.previous_button_clicked)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(previous_button)
        layout.addSpacing(20)
        layout.addWidget(self.idx_box)
        layout.addWidget(self.max_idx_label)
        layout.addSpacing(20)
        layout.addWidget(next_button)
        layout.addStretch(1)
        self.setLayout(layout)

    def set_max_idx(self, idx):
        self.max_idx = idx
        self.max_idx_label.setText('/ ' + str(idx + 1))
    
    def set_idx(self, idx):
        self.idx = idx
        self.idx_box.setText(str(idx + 1))
    
    def previous_button_clicked(self):
        if self.idx > 0:
            self.idxChanged.emit(self.idx - 1)
    
    def next_button_clicked(self):
        if self.idx < self.max_idx:
            self.idxChanged.emit(self.idx + 1)
    
    def idx_editing_finished(self):
        try:
            idx = int(self.idx_box.text()) - 1
            if idx < 0:
                self.idxChanged.emit(0)
            elif self.max_idx < idx:
                self.idxChanged.emit(self.max_idx)
            else:
                self.idxChanged.emit(idx)
        except:
            self.idx_box.setText(str(self.idx + 1))
        self.idx_box.clearFocus()

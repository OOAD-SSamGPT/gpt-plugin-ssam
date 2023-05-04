from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal

#위젯
class ScaleWidget(QWidget):
    scaleChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.scale = 1

        self.scale_box = QLineEdit('100', self)
        self.scale_box.setFixedWidth(60)
        self.scale_box.setAlignment(Qt.AlignCenter)
        self.scale_box.setFocusPolicy(Qt.ClickFocus)
        self.scale_box.editingFinished.connect(self.scale_editing_finished)

        percent_label = QLabel('%')
        percent_label.setAlignment(Qt.AlignCenter)

        zoom_in__button = QPushButton('+', self)
        zoom_in__button.setFocusPolicy(Qt.NoFocus)
        zoom_in__button.setFixedWidth(30)
        zoom_in__button.clicked.connect(self.zoom_in_button_clicked)

        zoom_out_button = QPushButton('-', self)
        zoom_out_button.setFocusPolicy(Qt.NoFocus)
        zoom_out_button.setFixedWidth(30)
        zoom_out_button.clicked.connect(self.zoom_out_button_clicked)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(zoom_in__button)
        layout.addSpacing(20)
        layout.addWidget(self.scale_box)
        layout.addWidget(percent_label)
        layout.addSpacing(20)
        layout.addWidget(zoom_out_button)
        layout.addStretch(1)
        self.setLayout(layout)
    
    def set_scale(self, scale):
        self.scale = scale
        self.scale_box.setText(f"{self.scale * 100:.2f}")
    
    def zoom_out_button_clicked(self):
        self.scaleChanged.emit(self.scale - 0.05)
    
    def zoom_in_button_clicked(self):
        self.scaleChanged.emit(self.scale + 0.05)
    
    def scale_editing_finished(self):
        try:
            scale = float(self.scale_box.text())
            if scale < 0.2:
                self.scaleChanged.emit(0.2)
            elif self.scale > 5:
                self.scaleChanged.emit(2)
            else:
                self.scaleChanged.emit(scale / 100)
        except:
            self.scale_box.setText(f"{self.scale * 100:.2f}")
        self.scale_box.clearFocus()

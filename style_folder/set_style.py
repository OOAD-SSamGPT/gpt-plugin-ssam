import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class SetStyle(QWidget):
    options_signal = pyqtSignal(str)
    additional_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.result = ""
        self.option_lst = []

        # 창 크기 및 위치 설정
        self.setGeometry(300, 300, 300, 250)

        # 수직 레이아웃 설정
        vbox = QVBoxLayout()

        # 수평 레이아웃 생성
        hbox = QHBoxLayout() #checkBox

        # 체크박스 생성
        self.checkbox1 = QCheckBox('자세히', self)
        hbox.addWidget(self.checkbox1)
        self.checkbox2 = QCheckBox('요약', self)
        hbox.addWidget(self.checkbox2)
        self.checkbox3 = QCheckBox('예시 포함', self)
        hbox.addWidget(self.checkbox3)
        self.checkbox4 = QCheckBox('최대한 길게', self)
        hbox.addWidget(self.checkbox4)
        self.checkbox5 = QCheckBox('전문적으로', self)
        hbox.addWidget(self.checkbox5)
        
        self.checkbox_lst = []
        self.checkbox_lst.append(self.checkbox1)
        self.checkbox_lst.append(self.checkbox2)
        self.checkbox_lst.append(self.checkbox3)
        self.checkbox_lst.append(self.checkbox4)
        self.checkbox_lst.append(self.checkbox5)
        
        for cb in self.checkbox_lst:
            cb.clicked.connect(self.change_option)

        # 수평 레이아웃을 수직 레이아웃에 추가
        vbox.addLayout(hbox)

        # 텍스트 박스 생성
        custom_box = QHBoxLayout()
        custom_label = QLabel('사용자 옵션 추가', self)
        self.textbox = QLineEdit(self)
        custom_box.addWidget(custom_label)
        custom_box.addWidget(self.textbox)

        self.textbox.returnPressed.connect(self.add_custom_option)
        vbox.addLayout(custom_box)

        #설정된 옵션 리스트 출력
        self.options = QLabel('', self)
        self.options.setAlignment(Qt.AlignCenter)
        font1 = self.options.font()
        font1.setPointSize(20)
        vbox.addWidget(self.options)
        
        #추천 질문 생성하기
        self.additional_checkbox = QCheckBox('추천 질문 생성', self)
        vbox.addWidget(self.additional_checkbox)

        # 버튼 생성
        button_box = QHBoxLayout()

        btn1 = QPushButton('옵션 초기화', self)
        button_box.addWidget(btn1)
        btn2 = QPushButton('스타일 저장', self)
        button_box.addWidget(btn2)

        
        btn1.clicked.connect(self.init_option)
        btn2.clicked.connect(self.save_option)

        vbox.addLayout(button_box)

        # 레이아웃 설정 적용
        self.setLayout(vbox)

        self.show()
    
    def add_custom_option(self):
        self.option_lst.append(self.textbox.text())
        self.options.setText(", ".join(self.option_lst))
        self.textbox.clear()

    def init_option(self):
        for cb in self.checkbox_lst:
            if cb.isChecked():
                cb.toggle()
        self.options.setText('')
        self.option_lst.clear()

    def change_option(self, state):
        for cb in self.checkbox_lst:
            if cb.isChecked():
                if cb.text() not in self.option_lst:
                    self.option_lst.append(cb.text())
            else:
                if cb.text() in self.option_lst:
                    self.option_lst.remove(cb.text())
        self.options.setText(", ".join(self.option_lst))

    
    def save_option(self):
        options = self.options.text() + ' 알려줘'
        self.options_signal.emit(options) #옵션 값 반환
        self.additional_signal.emit(self.additional_checkbox.isChecked()) #추가 질문 생성 여부 반환
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SetStyle()
    sys.exit(app.exec_())

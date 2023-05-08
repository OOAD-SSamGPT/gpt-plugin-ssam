from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NoteWidget(QTextEdit):

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.notes = []
    
    def load_notes(self, pdf):
        for page in pdf:
            for annot in page.annots():
                if annot.info['title'] == 'SsamGPT':
                    self.notes.append(annot.info['content'])
                    break
            else:
                self.notes.append('')
        self.set_idx(0)
    
    def set_idx(self, idx):
        self.setText(self.notes[idx])

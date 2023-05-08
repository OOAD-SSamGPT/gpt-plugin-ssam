from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NoteWidget(QTextEdit):

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.pages = []
        self.annots = []
        self.notes = []
        self.idx = 0

    def set_idx(self, idx):
        self.idx = idx
        self.setText(self.notes[idx])
    
    def load_notes(self, pdf):
        self.pages.clear()
        self.annots.clear()
        self.notes.clear()

        for page in pdf:
            self.pages.append(page)
            for annot in page.annots():
                if annot.info['title'] == 'SsamGPT':
                    self.notes.append(annot.info['content'])
                    self.annots.append(annot)
                    break
            else:
                self.notes.append('')
                self.annots.append(None)
        self.set_idx(0)
    
    def update_note(self):
        self.notes[self.idx] = self.toPlainText()
        self.clearFocus()

    def save_note(self):
        for i, page in enumerate(self.pages):
            if self.notes[i] != '':
                if self.annots[i]:
                    self.annots[i].set_info(content=self.notes[i])
                else:
                    annot = page.add_text_annot((-20, -20), self.notes[i])
                    annot.set_info(title='SsamGPT')
            elif self.annots[i]:
                page.delete_annot(self.annots[i])
        
            

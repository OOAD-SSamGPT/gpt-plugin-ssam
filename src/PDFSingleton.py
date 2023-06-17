class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class PDF(Singleton):
    def __init__(self):
       self.pdf = None
    
    def get_file(self):
        return self.pdf

    def set_file(self, pdf):
        self.pdf = pdf
    
    def get_page(self, idx):
        return self.pdf[idx]

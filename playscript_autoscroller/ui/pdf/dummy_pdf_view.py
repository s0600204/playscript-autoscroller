
from qtpy.QtWidgets import QWidget


class DummyPdfView(QWidget):

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application

    def clear(self):
        pass

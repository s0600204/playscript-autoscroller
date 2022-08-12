
from PyQt5.QtWidgets import QMenu


class ApplicationMenu(QMenu):

    def __init__(self, main_window, *args, **kwargs):
        super().__init__(parent=main_window.menubar, *args, **kwargs)

        self._window = main_window
        self._application = main_window._application
        self._actions = {}

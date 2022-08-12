
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMessageBox

from script_scroller import __app_name__
#from script_scroller.i18n import translate
from .menu import ApplicationMenu

def translate(_, text):
    return text

class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['fullscreen'] = QAction(self)
        self._actions['fullscreen'].setCheckable(True)
        self._actions['fullscreen'].triggered.connect(self._window.set_fullscreen)
        self.addAction(self._actions['fullscreen'])

        self.addSeparator()

        self._actions['exit'] = QAction(self)
        self._actions['exit'].triggered.connect(self._window.close)
        self.addAction(self._actions['exit'])

    def retranslate_ui(self):
        self.setTitle(translate("MainWindow", "&File"))

        self._actions['fullscreen'].setText(translate("MainWindow", "Full Screen"))
        self._actions['fullscreen'].setStatusTip(translate("MainWindow", "Toggle Full Screen"))
        if QKeySequence(QKeySequence.FullScreen).isEmpty():
            self._actions['fullscreen'].setShortcut("F11")
        else:
            self._actions['fullscreen'].setShortcut(QKeySequence.FullScreen)

        self._actions['exit'].setText(translate("MainWindow", "Exit"))
        self._actions['exit'].setStatusTip(translate("MainWindow", "Exit {}").format(__app_name__))
        self._actions['exit'].setShortcut(QKeySequence.Quit)


from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from script_scroller import __app_name__
#from script_scroller.i18n import translate
from .menu import ApplicationMenu

def translate(_, text):
    return text

class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['new'] = QAction(self)
        self._actions['new'].triggered.connect(self._application.file_new)
        self.addAction(self._actions['new'])

        self._actions['open'] = QAction(self)
        self._actions['open'].triggered.connect(self._application.file_open)
        self.addAction(self._actions['open'])

        self._actions['save'] = QAction(self)
        self._actions['save'].triggered.connect(self._application.file_save)
        self.addAction(self._actions['save'])

        self._actions['save_as'] = QAction(self)
        self._actions['save_as'].triggered.connect(self._application.file_save_as)
        self.addAction(self._actions['save_as'])

        self.addSeparator()

        self._actions['midi_config'] = QAction(self)
        self._actions['midi_config'].triggered.connect(self._window.open_midi_config)
        self.addAction(self._actions['midi_config'])

        self.addSeparator()

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

        self._actions['new'].setText(translate("MainWindow", "New"))
        self._actions['new'].setStatusTip(translate("MainWindow", "Create New File"))
        self._actions['new'].setShortcut(QKeySequence.New)

        self._actions['open'].setText(translate("MainWindow", "Open"))
        self._actions['open'].setStatusTip(translate("MainWindow", "Open a File"))
        self._actions['open'].setShortcut(QKeySequence.Open)

        self._actions['save'].setText(translate("MainWindow", "Save"))
        self._actions['save'].setStatusTip(translate("MainWindow", "Save the Current File"))
        self._actions['save'].setShortcut(QKeySequence.Save)

        self._actions['save_as'].setText(translate("MainWindow", "Save As..."))
        self._actions['save_as'].setStatusTip(translate("MainWindow", "Save the Current File with a Specific Name"))
        self._actions['save_as'].setShortcut(QKeySequence.SaveAs)

        self._actions['midi_config'].setText(translate("MainWindow", "Settings"))
        self._actions['midi_config'].setStatusTip(translate("MainWindow", "Open MIDI Config"))

        self._actions['fullscreen'].setText(translate("MainWindow", "Full Screen"))
        self._actions['fullscreen'].setStatusTip(translate("MainWindow", "Toggle Full Screen"))
        if QKeySequence(QKeySequence.FullScreen).isEmpty():
            self._actions['fullscreen'].setShortcut("F11")
        else:
            self._actions['fullscreen'].setShortcut(QKeySequence.FullScreen)

        self._actions['exit'].setText(translate("MainWindow", "Exit"))
        self._actions['exit'].setStatusTip(translate("MainWindow", "Exit {}").format(__app_name__))
        self._actions['exit'].setShortcut(QKeySequence.Quit)

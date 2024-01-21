
from qtpy.QtWidgets import (
    QAction,
    QApplication,
)

from playscript_autoscroller import __app_name__
from ..about_dialog import AboutDialog
#from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


def translate(_, text):
    return text


class AboutMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['about'] = QAction(self)
        self._actions['about'].triggered.connect(self._open_about)
        self.addAction(self._actions['about'])

        self._actions['aboutQt'] = QAction(self)
        self._actions['aboutQt'].triggered.connect(QApplication.aboutQt)
        self.addAction(self._actions['aboutQt'])

    def _open_about(self):
        about = AboutDialog(self._application, parent=self)
        about.retranslate_ui()
        about.exec()

    def retranslate_ui(self):
        self.setTitle(translate("MainWindow", "&About"))

        self._actions['about'].setText(translate("MainWindow", f"About {__app_name__}"))

        self._actions['aboutQt'].setText(translate("MainWindow", "About Qt"))

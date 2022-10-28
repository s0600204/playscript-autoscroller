
from PyQt5.QtWidgets import QAction

from playscript_autoscroller import __app_name__
#from playscript_autoscroller.i18n import translate
from ..toolbar_action import ToolbarAction
from .menu import ApplicationMenu

def translate(_, text):
    return text

class ImportMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['markdown'] = ToolbarAction(parent=self)
        self._actions['markdown'].triggered.connect(self.import_markdown)
        self._actions['markdown'].set_icon('markdown', 'markdown')
        self.addAction(self._actions['markdown'])

        self._actions['pdf'] = ToolbarAction(parent=self)
        self._actions['pdf'].triggered.connect(self.import_pdf)
        self._actions['pdf'].set_icon('pdf', 'adobeacrobatreader')
        self.addAction(self._actions['pdf'])

    def import_markdown(self):
        self._application.file_open_with_type('markdown')

    def import_pdf(self):
        self._application.file_open_with_type('pdf')

    def retranslate_ui(self):
        self.setTitle(translate("MainWindow", "Import"))

        self._actions['markdown'].setText(translate("MainWindow", "Markdown file"))
        self._actions['markdown'].setStatusTip(translate("MainWindow", "Import from a markdown file"))

        self._actions['pdf'].setText(translate("MainWindow", "PDF file"))
        self._actions['pdf'].setStatusTip(translate("MainWindow", "Import from a pdf file"))
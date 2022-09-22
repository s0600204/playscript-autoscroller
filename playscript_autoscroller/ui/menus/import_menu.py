
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

    def import_markdown(self):
        self._application.file_open_with_type('markdown')

    def retranslate_ui(self):
        self.setTitle(translate("MainWindow", "Import"))

        self._actions['markdown'].setText(translate("MainWindow", "Markdown file"))
        self._actions['markdown'].setStatusTip(translate("MainWindow", "Import from a markdown file"))


#from playscript_autoscroller.i18n import translate
from ...pdf import PDF_SUPPORT, PdfLibrary
from ..action_classes import MenuAction
from .menu import ApplicationMenu

def translate(_, text):
    return text

class ImportMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['markdown'] = MenuAction(self)
        self._actions['markdown'].triggered.connect(self.import_markdown)
        self._actions['markdown'].set_icon('markdown')
        self.addAction(self._actions['markdown'])

        self._actions['pdf'] = MenuAction(self)
        self._actions['pdf'].triggered.connect(self.import_pdf)
        self._actions['pdf'].set_icon('adobeacrobatreader')
        self._actions['pdf'].setEnabled(bool(PDF_SUPPORT is not PdfLibrary.Disabled))
        self.addAction(self._actions['pdf'])

    def import_markdown(self):
        self._application.file_open_with_type('markdown')

    def import_pdf(self):
        self._application.file_open_with_type('pdf')

    def retranslate_ui(self):
        self.setTitle(translate("MainWindow", "Import"))

        self._actions['markdown'].setText(
            translate("MainWindow", "Markdown file"))
        self._actions['markdown'].setStatusTip(
            translate("MainWindow", "Import from a markdown file"))

        self._actions['pdf'].setText(
            translate("MainWindow", "PDF file"))
        self._actions['pdf'].setStatusTip(
            translate("MainWindow", "Import from a pdf file"))

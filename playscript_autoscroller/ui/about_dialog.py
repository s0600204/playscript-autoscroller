
import sys

import qtpy
from qtpy.QtCore import (
    QSize,
    Qt,
    qVersion,
)
if qtpy.QT5:
    from qtpy.QtSvg import QSvgWidget
else:
    from qtpy.QtSvgWidgets import QSvgWidget
from qtpy.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)

import rtmidi

from ..pdf import PDF_SUPPORT, PdfLibrary
if PDF_SUPPORT is PdfLibrary.Poppler:
    import popplerqt5

from playscript_autoscroller import ( # pylint: disable=wrong-import-order
    __app_icon__,
    __app_name__,
    __doc__,
    __version__,
)
from .action_classes import SvgIconWidget


class SubIcons(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self._icon_qt = SvgIconWidget(self)
        self._icon_qt.set_icon('qt')
        self._icon_qt.set_size(24)
        self.layout().addWidget(self._icon_qt)

        self._icon_python = SvgIconWidget(self)
        self._icon_python.set_icon('python')
        self._icon_python.set_size(24)
        self.layout().addWidget(self._icon_python)

        self._icon_midi = SvgIconWidget(self)
        self._icon_midi.set_icon('midi')
        self._icon_midi.set_size(24)
        self.layout().addWidget(self._icon_midi)

        if PDF_SUPPORT is not PdfLibrary.Disabled:
            self._icon_pdf = SvgIconWidget(self)
            self._icon_pdf.set_icon('adobeacrobatreader')
            self._icon_pdf.set_size(24)
            self.layout().addWidget(self._icon_pdf)

    def retranslate_ui(self):
        if qtpy.PYSIDE2 or qtpy.PYSIDE6:
            binding_version = f"{qtpy.API_NAME} {qtpy.PYSIDE_VERSION}"
        else:
            binding_version = f"{qtpy.API_NAME} {qtpy.PYQT_VERSION}"
        self._icon_qt.setToolTip(f"Qt {qVersion()}\n{binding_version}")
        self._icon_python.setToolTip(f"python {sys.version.split(maxsplit=1)[0]}")
        self._icon_midi.setToolTip(
            f"rtmidi {rtmidi.get_rtmidi_version()}\npython-rtmidi {rtmidi.version.version}")
        if PDF_SUPPORT is PdfLibrary.Poppler:
            poppler_version = '.'.join([str(x) for x in popplerqt5.poppler_version()])
            self._icon_pdf.setToolTip(f"(PDF support by) Poppler {poppler_version}")

class AboutDialog(QDialog):

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._application = application
        self.setLayout(QGridLayout())
        self.layout().setSizeConstraint(QGridLayout.SetFixedSize)

        self._icon = QSvgWidget(self)
        self._icon.load(__app_icon__)
        self._icon.setMinimumSize(QSize(128, 128))
        self.layout().addWidget(self._icon, 0, 0, 5, 1)
        self.layout().setAlignment(self._icon, Qt.AlignCenter)

        self._subicons = SubIcons(self)
        self.layout().addWidget(self._subicons, 5, 0)

        self._caption_name = QLabel(self)
        self._caption_name.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.layout().addWidget(self._caption_name, 1, 1)
        self.layout().setAlignment(self._caption_name, Qt.AlignBottom)

        self._caption_desc = QLabel(self)
        self._caption_desc.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._caption_desc, 2, 1)

        self._caption_version = QLabel(self)
        self._caption_version.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout().addWidget(self._caption_version, 3, 1)
        self.layout().setAlignment(self._caption_version, Qt.AlignTop)

        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(QDialogButtonBox.Ok)
        self._button_box.accepted.connect(self.accept)
        self.layout().addWidget(self._button_box, 5, 1)

    def retranslate_ui(self):
        self.setWindowTitle(f"About {__app_name__}")
        self._caption_name.setText(f"<h2>{__app_name__}</h2>")
        self._caption_desc.setText(__doc__)
        self._caption_version.setText(__version__)
        self._subicons.retranslate_ui()

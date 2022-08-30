
from PyQt5.Qt import (
    QSize,
    Qt,
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
)

from script_scroller import (
    __app_icon__,
    __app_name__,
    __doc__,
    __version__,
)


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
        self.layout().addWidget(self._button_box, 4, 1, 1, 1)

    def retranslate_ui(self):
        self.setWindowTitle(f"About {__app_name__}")
        self._caption_name.setText(f"<h2>{__app_name__}</h2>")
        self._caption_desc.setText(__doc__)
        self._caption_version.setText(__version__)


from os import path

from qtpy.QtCore import Signal as QSignal, QSize
from qtpy.QtGui import QIcon, QPainter
from qtpy.QtWidgets import QAction, QToolButton, QWidget

from .palette_icon_engine import PaletteIconEngine


class _Action:

    enabled = QSignal(bool)

    BundledIconSubPath = "icons"
    BundledIconsets = [
        "lucide",
        "simpleicons",
        "own",
    ]

    def _build_icon(self, icon_name, icon_name_checked=None):
        icon = QIcon(PaletteIconEngine(self.parent().palette)) # pylint: disable=no-member

        icon_path = self._find_icon(icon_name)
        if icon_path:
            icon.addFile(icon_path)

        if icon_name_checked:
            icon_path = self._find_icon(icon_name_checked)
            if icon_path:
                icon.addFile(icon_path, state=QIcon.On)

        return icon

    def _find_icon(self, icon_name):
        icon_path = path.join(path.dirname(__file__), self.BundledIconSubPath)
        for iconset in self.BundledIconsets:
            search_path = path.join(icon_path, iconset, icon_name + '.svg')
            if path.exists(search_path):
                return search_path
        return None

    def set_icon(self, name, name_checked=None):
        self.setIcon(self._build_icon(name, name_checked)) # pylint: disable=no-member


class MenuAction(QAction, _Action):
    pass

class ToolbarAction(QAction, _Action):

    def setEnabled(self, enabled: bool): # pylint: disable=invalid-name
        super().setEnabled(enabled)
        self.enabled.emit(enabled)

class ToolButtonAction(QToolButton, _Action):
    pass

class SvgIconWidget(QWidget, _Action):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icon = None
        self._pixmap = None

    def set_icon(self, name): # pylint: disable=arguments-differ
        self._icon = self._build_icon(name, None)
        self._pixmap = None

    def set_size(self, breadth):
        size = QSize(breadth, breadth)
        self.setMinimumSize(size)
        self.setMaximumSize(size)
        self._pixmap = None

    def paintEvent(self, _): # pylint: disable=invalid-name
        if not self._pixmap:
            self._pixmap = self._icon.pixmap(self.size())

        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self._pixmap)
        painter.end()

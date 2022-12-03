
from os import path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from .palette_icon_engine import PaletteIconEngine


class _Action:

    enabled = pyqtSignal(bool)

    BundledIconSubPath = "icons"
    BundledIconsets = [
        "lucide",
        "simpleicons",
        "own",
    ]

    def _build_icon(self, icon_name, icon_name_checked=None):
        icon = QIcon(PaletteIconEngine(self.parent().palette))

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
        self.setIcon(self._build_icon(name, name_checked))


class MenuAction(QAction, _Action):
    pass

class ToolbarAction(QAction, _Action):

    def setEnabled(self, enabled: bool): # pylint: disable=invalid-name
        super().setEnabled(enabled)
        self.enabled.emit(enabled)

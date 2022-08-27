
from os import path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


class ToolbarAction(QAction):

    BundledIconSubPath = "icons"

    def _find_icon_local(self, system_name, bundled_name=None, bundled_name_checked=None):

        if not bundled_name:
            return QIcon(path.join(path.dirname(__file__), self.BundledIconSubPath, system_name))

        icon = QIcon(path.join(path.dirname(__file__), self.BundledIconSubPath, bundled_name))

        if bundled_name_checked:
            icon.addFile(
                path.join(path.dirname(__file__), self.BundledIconSubPath, bundled_name_checked),
                state=QIcon.On)

        return icon

    def _find_icon_system(self, icon_name):
        if QIcon.hasThemeIcon(icon_name):
            return QIcon.fromTheme(icon_name)

        icon_name_symbolic = f"{icon_name}-symbolic"
        if QIcon.hasThemeIcon(icon_name_symbolic):
            return QIcon.fromTheme(icon_name_symbolic)

        return None

    def set_icon(self, system_name, bundled_name=None, bundled_name_checked=None):
        icon = self._find_icon_system(system_name)

        if not icon:
            icon = self._find_icon_local(system_name, bundled_name, bundled_name_checked)

        self.setIcon(icon)

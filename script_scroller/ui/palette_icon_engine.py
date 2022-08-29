# custom icon engine Qt plugin
# Copyright (C) 2017-2020  Nick Korotysh <nick.korotysh@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Transcoded from the discontinued Palette Icon Engine by Kolcha:
#   https://github.com/Kolcha/paletteicon   (GPL-3.0)

# pylint: disable=invalid-name

from os import path

from PyQt5.QtCore import (
    QSize,
    Qt,
)
from PyQt5.QtGui import (
    QColor,
    QIcon,
    QIconEngine,
    QPainter,
    QPalette,
    QPixmap,
    QPixmapCache,
)
from PyQt5.QtSvg import (
    QSvgRenderer,
)


class PaletteIconEngine(QIconEngine):

    def __init__(self, other=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._renderer = QSvgRenderer()
        self._src_file = None

        if other and other._renderer.isValid():
            self._renderer.load(other._src_file)
            self._src_file = other._src_file

    # @param filename string
    # @return string
    @staticmethod
    def _actual_filename(filename):
        if path.exists(filename):
            return filename
        return f"{filename}.svg"

    # @param mode  QIcon.Mode
    # @param state QIcon.state (UNUSED)
    @staticmethod
    def getIconColor(mode, state):
        color_group = QPalette.Active
        if mode == QIcon.Disabled:
            color_group = QPalette.Disabled
        return QPalette().color(color_group, QPalette.WindowText)

    # @param renderer QSvgRenderer
    # @param size     QSize
    # @param brush    QBrush
    # @return QPixmap
    @staticmethod
    def renderIcon(renderer, size, brush):
        output = QPixmap(size)
        output.fill(Qt.transparent)

        painter = QPainter(output)
        renderer.render(painter)

        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(output.rect())

        return output

    # @param filename string
    # @param size     QSize (UNUSED)
    # @param mode     QIcon.Mode (UNUSED)
    # @param state    QIcon.State (UNUSED)
    def addFile(self, filename, size, mode, state):
        filename = self._actual_filename(filename)
        if filename == self._src_file:
            return
        if self._renderer.load(filename):
            self._src_file = filename

    # @return QIconEngine
    def clone(self):
        return PaletteIconEngine(self)

    # @param mode  QIcon.Mode (UNUSED)
    # @param state QIcon.State (UNUSED)
    # @return list(QSize)
    def availableSizes(self, mode, state):
        return [
            # KOLCHA COMMENT:
            #   just workaround to make tray icon visible on KDE
            QSize(512, 512),
        ]

    # @param painter QPainter
    # @param rect    QRect
    # @param mode    QIcon.Mode
    # @param state   QIcon.State
    def paint(self, painter, rect, mode, state):
        # KOLCHA COMMENT:
        #   "direct rendereng" using given painter is not possible
        #   because colorization logic modifies already painted area
        #   such behavior is not acceptable, so render icon to pixmap first
        color = self.getIconColor(mode, state)
        out = self.renderIcon(
            self._renderer,
            rect.size() * painter.device().devicePixelRatioF(),
            color)
        out.setDevicePixelRatio(painter.device().devicePixelRatioF())
        painter.drawPixmap(rect, out)

    # @param size  QSize
    # @param mode  QIcon.Mode
    # @param state QIcon.State
    # @return QPixmap
    def pixmap(self, size, mode, state):
        color = self.getIconColor(mode, state)
        pmckey = "pie_{}:{}x{}:{}-{}{}".format(
            self._src_file,
            size.width(),
            size.height(),
            mode,
            state,
            color.name(QColor.HexArgb))

        pxm = QPixmapCache.find(pmckey)
        if not pxm:
            pxm = self.renderIcon(self._renderer, size, color)
            QPixmapCache.insert(pmckey, pxm)
        return pxm

    # @param id int
    # @param data
    def virtual_hook(self, id, data):
        if id == QIconEngine.IsNullHook:
            data = not self._renderer or not self._renderer.isValid()
            return

        super().virtual_hook(id, data)

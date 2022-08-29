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

    def __init__(self, palette_getter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._palette = palette_getter
        self._renderer = QSvgRenderer()
        self._src_files = {}

    # @param filename string
    # @return string
    @staticmethod
    def _actual_filename(filename):
        if path.exists(filename):
            return filename
        return f"{filename}.svg"

    # @param mode    QIcon.Mode
    # @param state   QIcon.state (UNUSED)
    def _get_icon_color(self, mode, state):
        color_group = QPalette.Active
        if mode == QIcon.Disabled:
            color_group = QPalette.Disabled
        return self._palette().color(color_group, QPalette.WindowText)

    # @param mode    QIcon.Mode
    # @param state   QIcon.state
    def _get_icon_src(self, mode, state):
        def _find(key, icon):
            if key in self._src_files:
                icon.append(self._src_files[key])
            return icon

        response = []
        # If we have a specific image to have, use it.
        if _find((mode, state), response):
            return response[0]

        # Else find a suitable alternative, based on the table found on
        # https://doc.qt.io/qt-5/qtwidgets-widgets-icons-example.html
        opposite_state = QIcon.Off if state == QIcon.On else QIcon.Off
        if mode in (QIcon.Normal, QIcon.Active):
            opposite_mode = QIcon.Active if mode == QIcon.Normal else QIcon.Normal
            if _find((opposite_mode, state), response):
                return response[0]
            if _find((mode, opposite_state), response):
                return response[0]
            if _find((opposite_mode, opposite_state), response):
                return response[0]
            if _find((QIcon.Disabled, state), response):
                return response[0]
            if _find((QIcon.Selected, state), response):
                return response[0]
            if _find((QIcon.Disabled, opposite_state), response):
                return response[0]
            if _find((QIcon.Selected, opposite_state), response):
                return response[0]
        else:
            opposite_mode = QIcon.Disabled if QIcon.Selected else QIcon.Selected
            if _find((QIcon.Normal, state), response):
                return response[0]
            if _find((QIcon.Active, state), response):
                return response[0]
            if _find((mode, opposite_state), response):
                return response[0]
            if _find((QIcon.Normal, opposite_state), response):
                return response[0]
            if _find((QIcon.Active, opposite_state), response):
                return response[0]
            if _find((opposite_mode, state), response):
                return response[0]
            if _find((opposite_mode, opposite_state), response):
                return response[0]

        return None

    # @param renderer QSvgRenderer
    # @param size     QSize
    # @param brush    QBrush
    # @return QPixmap
    @staticmethod
    def _render_icon(renderer, filename, size, brush):
        output = QPixmap(size)
        output.fill(Qt.transparent)

        painter = QPainter(output)
        renderer.load(filename)
        renderer.render(painter)

        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(output.rect())

        return output

    # @param filename string
    # @param size     QSize (UNUSED)
    # @param mode     QIcon.Mode
    # @param state    QIcon.State
    def addFile(self, filename, size, mode, state):
        filename = self._actual_filename(filename)
        key = (mode, state)
        if key in self._src_files and filename == self._src_files[key]:
            return
        self._src_files[key] = filename

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
        filename = self._get_icon_src(mode, state)
        color = self._get_icon_color(mode, state)
        out = self._render_icon(
            self._renderer,
            filename,
            rect.size() * painter.device().devicePixelRatioF(),
            color)
        out.setDevicePixelRatio(painter.device().devicePixelRatioF())
        painter.drawPixmap(rect, out)

    # @param size  QSize
    # @param mode  QIcon.Mode
    # @param state QIcon.State
    # @return QPixmap
    def pixmap(self, size, mode, state):
        filename = self._get_icon_src(mode, state)
        color = self._get_icon_color(mode, state)
        pmckey = "pie_{}:{}x{}:{}-{}{}".format(
            filename,
            size.width(),
            size.height(),
            mode,
            state,
            color.name(QColor.HexArgb))

        pxm = QPixmapCache.find(pmckey)
        if not pxm:
            pxm = self._render_icon(self._renderer, filename, size, color)
            QPixmapCache.insert(pmckey, pxm)
        return pxm

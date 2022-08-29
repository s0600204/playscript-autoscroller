# "Palette Icon Engine"; transcoded and adapted from the original C++.
# Original source: https://github.com/Kolcha/paletteicon
#
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


from os import path

from PyQt5.QtCore import (
    QRect,
    QSize,
    Qt,
)
from PyQt5.QtGui import (
    QBrush,
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

    @staticmethod
    def _actual_filename(filename: str) -> str:
        if path.exists(filename):
            return filename
        return f"{filename}.svg"

    def _get_icon_color(self,
                        mode: QIcon.Mode) -> QColor:
        color_group = QPalette.Active
        if mode == QIcon.Disabled:
            color_group = QPalette.Disabled
        return self._palette().color(color_group, QPalette.WindowText)

    def _get_icon_src(self,
                      mode: QIcon.Mode,
                      state: QIcon.State) -> str:
        # pylint: disable=too-many-branches, too-many-return-statements

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

    def _render_icon(self,
                     filename: str,
                     size: QSize,
                     brush: QBrush) -> QPixmap:
        output = QPixmap(size)
        output.fill(Qt.transparent)

        painter = QPainter(output)
        self._renderer.load(filename)
        self._renderer.render(painter)

        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(output.rect())

        return output

    def addFile(self,
                filename: str,
                _, # (size: QSize)
                mode: QIcon.Mode,
                state: QIcon.State):
        # pylint: disable=invalid-name

        filename = self._actual_filename(filename)
        key = (mode, state)
        if key in self._src_files and filename == self._src_files[key]:
            return
        self._src_files[key] = filename

    # (Unused Args:: mode: QIcon.Mode, state: QIcon.State)
    # (Actual return:: list of QSize)
    def availableSizes(self, *_) -> list:
        # pylint: disable=invalid-name

        return [
            # ORIGINAL AUTHOR COMMENT:
            #   just workaround to make tray icon visible on KDE
            QSize(512, 512),
        ]

    def paint(self,
              painter: QPainter,
              rect: QRect,
              mode: QIcon.Mode,
              state: QIcon.State):
        # ORIGINAL AUTHOR COMMENT:
        #   "direct rendereng" using given painter is not possible
        #   because colorization logic modifies already painted area
        #   such behavior is not acceptable, so render icon to pixmap first
        filename = self._get_icon_src(mode, state)
        color = self._get_icon_color(mode)
        out = self._render_icon(
            filename,
            rect.size() * painter.device().devicePixelRatioF(),
            color)
        out.setDevicePixelRatio(painter.device().devicePixelRatioF())
        painter.drawPixmap(rect, out)

    def pixmap(self,
               size: QSize,
               mode: QIcon.Mode,
               state: QIcon.State) -> QPixmap:
        filename = self._get_icon_src(mode, state)
        color = self._get_icon_color(mode)

        # pylint: disable=consider-using-f-string
        pmckey = "pie_{}:{}x{}:{}-{}{}".format(
            filename,
            size.width(),
            size.height(),
            mode,
            state,
            color.name(QColor.HexArgb))

        pxm = QPixmapCache.find(pmckey)
        if not pxm:
            pxm = self._render_icon(filename, size, color)
            QPixmapCache.insert(pmckey, pxm)
        return pxm

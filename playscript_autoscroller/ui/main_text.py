
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QFont,
    QFontMetrics,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt5.QtWidgets import (
    QShortcut
)

from pyqt5_rst import QRstTextEdit


class MainText(QRstTextEdit):

    DefaultZoom = 1

    def __init__(self, application, toolbar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application
        self._toolbar = toolbar

        # According to the CommonMark MarkDown spec, tabs used at the start of a line as
        # indentation should each be replaced with an indent of four spaces.
        # The replacement is done by Qt5, but this also gives a reference for how wide tabs
        # should be.
        metrics = QFontMetrics(self.currentFont())
        self.setTabStopDistance(metrics.horizontalAdvance(" ") * 4)

        # See comment of connected method for explanation of this.
        if sys.platform == "linux":
            shifttab_shortcut = QShortcut("Shift+Tab", self)
            shifttab_shortcut.setContext(Qt.WidgetShortcut)
            shifttab_shortcut.activated.connect(self._tab_handling)

        self._base_font_size = self.currentFont().pointSize()
        self._zoom_level = self._application.register_config('zoom', self.DefaultZoom)
        self._application.config_restored.connect(self.zoom)

        self.cursorPositionChanged.connect(self.on_cursor_move)
        self.textChanged.connect(application.set_dirty)

    @property
    def content(self):
        return self.toReStructuredText()

    @property
    def cursor(self):
        return self._cursor

    @property
    def toolbar(self):
        return self._toolbar

    def _tab_handling(self, shift_down=True):
        """
        Does the actual work of tab customisation behaviour.

        This exists because on Linux - even with `self.tabChangesFocus == False` - Shift+Tab
        changes focus. (Works fine on Windows 10. macOS is untested at this time.)

        Thus: on Linux we setup a widget-level shortcut that intercepts the Shift+Tab key
        combination and diverts it here. The keyPressEvent method below hands off to this to
        minimise code duplication.

        If Qt ever fixes this, we can remove this work-around.
        """
        cursor = self.textCursor()
        if cursor.atBlockStart():
            if shift_down:
                self.dedent()
            else:
                self.indent()
            self.on_cursor_move()
            return True

        if shift_down:
            cursor.movePosition(QTextCursor.Left, n=4)
            self.setTextCursor(cursor)
            return True

        return False

    def currentBlockFormat(self):
        # pylint: disable=invalid-name
        cursor = self.textCursor()
        return cursor.blockFormat()

    def dedent(self):
        block_format = self.currentBlockFormat()
        indent = block_format.indent()
        if indent > 0:
            indent -= 1
            block_format.setIndent(indent)
            self.setCurrentBlockFormat(block_format)
        return indent

    def go_to_position(self, position):
        cursor = self.textCursor()

        # Jump to the end of the document before going where we want,
        # so that we end up with where we want at the top of the viewport.
        cursor.setPosition(self.document().lastBlock().position())
        self.setTextCursor(cursor)

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

    def indent(self):
        block_format = self.currentBlockFormat()
        indent = block_format.indent() + 1
        block_format.setIndent(indent)
        self.setCurrentBlockFormat(block_format)

    def keyPressEvent(self, event): # pylint: disable=invalid-name
        """
        Function overridden so as to customise tab behaviour:

        * Tabbing when at the *start* of a line will indent the text;
        * Shift-tabbing when at the *start* of a line will deindent the text;
        * Shift-tabbing in the *middle* of a line will move the cursor back.
        """
        if event.text() == "\t":
            shift_down = event.modifiers() & Qt.ShiftModifier
            if self._tab_handling(shift_down):
                return

        super().keyPressEvent(event)

    def on_cursor_move(self):
        block_format = self.currentBlockFormat()
        char_format = self.currentCharFormat()
        style = {
            "bold": char_format.fontWeight() == QFont.Bold,
            "italic": char_format.fontItalic(),
            "underline": char_format.fontUnderline(),
            "strikethrough": char_format.fontStrikeOut(),
            "indent": block_format.indent(),
        }
        self._toolbar.update_style_buttons(style)

    def respace_text(self):
        # Set Paragraph Spacing
        #   This is dependant on each paragraph's formatting (header, normal text).
        #   A better way of doing this might be to subclass QAbstractTextDocumentLayout.
        block = self.document().begin()
        level_spacing = {}
        was_dirty = self._application.is_dirty()
        while block.isValid():
            block_cursor = QTextCursor(block)
            block_format = block.blockFormat()
            block_level = block_format.headingLevel()

            if block_level not in level_spacing:
                char_format = block_cursor.charFormat()
                font = char_format.font()
                level_spacing[block_level] = QFontMetrics(font).height() * 0.5

            block_format.setTopMargin(level_spacing[block_level])
            block_cursor.setBlockFormat(block_format)
            block = block.next()

        # Annoyingly, the above is considered "changing the text", thus when the above is run
        # as part of the application init, the supposedly "new" document is considered dirty.
        if not was_dirty:
            self._application.set_clean()

    def scroll(self, step):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + step)

    def setCurrentBlockFormat(self, block_format):
        # pylint: disable=invalid-name
        cursor = self.textCursor()
        return cursor.setBlockFormat(block_format)

    def setFontBold(self, checked):
        # pylint: disable=invalid-name
        if checked:
            self.setFontWeight(QFont.Bold)
        else:
            self.setFontWeight(QFont.Normal)

    def setFontStrikeThrough(self, checked):
        # pylint: disable=invalid-name
        style = self.currentCharFormat()
        style.setFontStrikeOut(checked)
        self.setCurrentCharFormat(style)

    def show_source_view(self, show):
        # The position multiplication is used to roughly place the cursor back where it was.
        # It's not very accurate, and will get worse the further down a document the cursor is
        # when a transition occurs.
        cursor = self.textCursor()
        position = cursor.position()
        was_dirty = self._application.is_dirty()

        if show:
            # We have to set the position to 0 before clearing the text formatting, else any
            # text selected before the transition will have its formatting stripped.
            cursor.setPosition(0)
            self.setTextCursor(cursor)

            position *= 1.5
            self.setCurrentCharFormat(QTextCharFormat())
            self.setPlainText(self.toReStructuredText())
        else:
            position /= 1.5
            self.setReStructuredText(self.toPlainText())
            self.respace_text()

        # Reset to clean if the document content hadn't actually been changed previously
        if not was_dirty:
            self._application.set_clean()

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

    def zoom(self):
        font = self.document().defaultFont()
        font.setPointSize(self._base_font_size + self._zoom_level())
        self.document().setDefaultFont(font)
        self.respace_text()

    def zoom_in(self, _):
        level = self._zoom_level()
        if level >= 50:
            return
        self._application.save_config('zoom', level + 1)
        self.zoom()

    def zoom_out(self, _):
        level = self._zoom_level()
        if level <= 1:
            return
        self._application.save_config('zoom', level - 1)
        self.zoom()

    def zoom_reset(self, _):
        self._application.save_config('zoom', 1)
        self.zoom()


import sys

from qtpy.QtCore import Qt
from qtpy.QtGui import (
    QFont,
    QFontDatabase,
    QFontMetrics,
    QTextCharFormat,
    QTextCursor,
)
from qtpy.QtWidgets import (
    QShortcut
)

from rst4qt import QRstTextEdit


class MainText(QRstTextEdit):

    DefaultZoom = 1
    NormalIndentWidth = 4
    ZoomConfigKey = 'zoom_text'
    HeadingSizeMagic = 4

    def __init__(self, application, toolbar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application
        self._toolbar = toolbar

        # See comment of connected method for explanation of this.
        if sys.platform == "linux":
            shifttab_shortcut = QShortcut("Shift+Tab", self)
            shifttab_shortcut.setContext(Qt.WidgetShortcut)
            shifttab_shortcut.activated.connect(self._tab_handling)

        self._normal_font = self.font()
        self._mono_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self._mono_font.setStyleHint(QFont.Monospace)

        self._base_font_size = self.currentFont().pointSize()
        self._zoom_level = self._application.register_config(self.ZoomConfigKey, self.DefaultZoom)
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

        if self._application.window.source_view_active:
            # "Source View" active: indent with 2 spaces, per the RST specification
            ws_len = 0
            for char in cursor.block().text():
                if char != ' ':
                    break
                ws_len += 1

            if cursor.atBlockStart() or cursor.positionInBlock() <= ws_len:
                diff = ws_len % 2 or 2
                if shift_down:
                    if ws_len:
                        cursor.movePosition(
                            QTextCursor.PreviousCharacter,
                            QTextCursor.KeepAnchor,
                            diff)
                        cursor.removeSelectedText()
                else:
                    cursor.insertText(' ' * diff)
                self.on_cursor_move()
                return True

        else:
            # "Source View" not active: indent normally
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

    def clear_format(self, _):
        self.setFontBold(False)
        self.setFontItalic(False)
        self.setFontUnderline(False)
        self.setFontStrikeThrough(False)
        self.setFontMonospace(False)
        self.on_cursor_move()

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
            "monospace": char_format.font().styleHint() == QFont.Monospace,
            "indent": block_format.indent(),
            "heading_level": block_format.headingLevel(),
        }
        self._toolbar.update_style_buttons(style)

    def respace_text(self):
        document = self.document()

        # Remove the ability for the user to "undo" the respacing.
        previous_undo_redo_state = document.isUndoRedoEnabled()
        document.setUndoRedoEnabled(False)

        block = document.begin()
        block_cursor = QTextCursor(block)

        # Group the entire respacing work into one "edit block", greatly reducing the time taken
        # by this method to complete (~6.5-7.9s ==> ~0.08-0.10s).
        block_cursor.beginEditBlock()

        # Set Paragraph Spacing
        #   This is dependant on each paragraph's formatting (header, normal text).
        #   A better way of doing this might be to subclass QAbstractTextDocumentLayout.
        level_spacing = {}
        was_dirty = self._application.is_dirty()
        while block.isValid():
            block_format = block.blockFormat()
            block_level = block_format.headingLevel()

            if block_level not in level_spacing:
                char_format = block_cursor.charFormat()
                font = char_format.font()
                level_spacing[block_level] = QFontMetrics(font).height() * 0.5

            # Update the size of monospaced sections
            for form in block.textFormats():
                if form.format.font().styleHint() == QFont.Monospace:
                    start = block.position() + form.start
                    end = start + form.length
                    block_cursor.setPosition(start)
                    block_cursor.setPosition(end, QTextCursor.KeepAnchor)
                    fmt = form.format
                    fmt.setFont(self._mono_font)
                    block_cursor.setCharFormat(fmt)

            block_format.setTopMargin(level_spacing[block_level])
            block_cursor.setBlockFormat(block_format)
            block = block.next()
            block_cursor = QTextCursor(block)

        block_cursor.endEditBlock()
        document.setUndoRedoEnabled(previous_undo_redo_state)

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
            self.setFontItalic(False)
            self.setFontMonospace(False)
            self.setFontStrikeThrough(False)
            self.setFontUnderline(False)

            if self.fontWeight() != QFont.Bold:
                self.setFontWeight(QFont.Bold)
        else:
            if self.fontWeight() != QFont.Normal:
                self.setFontWeight(QFont.Normal)
        self.on_cursor_move()

    def setFontItalic(self, checked):
        # pylint: disable=invalid-name
        if checked:
            self.setFontBold(False)
            self.setFontMonospace(False)
            self.setFontStrikeThrough(False)
            self.setFontUnderline(False)

        if self.fontItalic() != checked:
            super().setFontItalic(checked)
        self.on_cursor_move()

    def setFontMonospace(self, checked):
        # pylint: disable=invalid-name
        font_style_hint = self.currentFont().styleHint()
        if checked:
            self.setFontBold(False)
            self.setFontItalic(False)
            self.setFontStrikeThrough(False)
            self.setFontUnderline(False)

            if font_style_hint != QFont.Monospace:
                self.setCurrentFont(self._mono_font)
        elif font_style_hint == QFont.Monospace:
            self.setCurrentFont(self._normal_font)
        self.on_cursor_move()

    def setFontStrikeThrough(self, checked):
        # pylint: disable=invalid-name
        if checked:
            self.setFontBold(False)
            self.setFontItalic(False)
            self.setFontMonospace(False)
            self.setFontUnderline(False)

        style = self.currentCharFormat()
        if style.fontStrikeOut() != checked:
            style.setFontStrikeOut(checked)
            self.setCurrentCharFormat(style)
        self.on_cursor_move()

    def setFontUnderline(self, checked):
        # pylint: disable=invalid-name
        if checked:
            self.setFontBold(False)
            self.setFontItalic(False)
            self.setFontMonospace(False)
            self.setFontStrikeThrough(False)

        if self.fontUnderline() != checked:
            super().setFontUnderline(checked)
        self.on_cursor_move()

    def setTextHeadingLevel(self, level):
        # pylint: disable=invalid-name
        block_format = self.currentBlockFormat()
        block_format.setHeadingLevel(level)
        self.setCurrentBlockFormat(block_format)

        # Update visual appearance of text
        char_format = QTextCharFormat()
        char_format.setProperty(
            QTextCharFormat.FontSizeAdjustment,
            level and self.HeadingSizeMagic - level or 0)
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.mergeCharFormat(char_format)

        self.on_cursor_move()

    def show_source_view(self, show):
        # The position multiplication is used to roughly place the cursor back where it was.
        # It's not very accurate, and will get worse the further down a document the cursor is
        # when a transition occurs.
        cursor = self.textCursor()
        position = cursor.position()
        was_dirty = self._application.is_dirty()

        # plaintext pastes only in Source View
        self.setAcceptRichText(not show)

        if show:
            # We have to set the position to 0 before clearing the text formatting, else any
            # text selected before the transition will have its formatting stripped.
            cursor.setPosition(0)
            self.setTextCursor(cursor)

            position *= 1.5
            self.setCurrentCharFormat(QTextCharFormat())
            self.setPlainText(self.toReStructuredText())
            self.setFont(self._mono_font)
            self.update_tab_stop_distance(self._mono_font)
        else:
            position /= 1.5
            self.setFont(self._normal_font)
            self.update_tab_stop_distance(self._normal_font)
            self.setReStructuredText(self.toPlainText())
            self.respace_text()

        # Reset to clean if the document content hadn't actually been changed previously
        if not was_dirty:
            self._application.set_clean()

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

    def update_tab_stop_distance(self, font):
        distance = QFontMetrics(font).horizontalAdvance(" ")
        if self._application.window.source_view_active:
            # Tab width of 2, per the RST specification
            distance *= 2
        else:
            distance *= self.NormalIndentWidth
        self.setTabStopDistance(distance)

    def zoom(self):
        self._normal_font.setPointSize(self._base_font_size + self._zoom_level())
        self._mono_font.setPointSize(self._base_font_size + self._zoom_level())
        if self._application.window.source_view_active:
            self.setFont(self._mono_font)
            self.update_tab_stop_distance(self._mono_font)
        else:
            self.setFont(self._normal_font)
            self.update_tab_stop_distance(self._normal_font)
        self.respace_text()

    def zoom_in(self):
        level = self._zoom_level()
        if level >= 50:
            return
        self._application.save_config(self.ZoomConfigKey, level + 1)
        self.zoom()

    def zoom_out(self):
        level = self._zoom_level()
        if level <= 1:
            return
        self._application.save_config(self.ZoomConfigKey, level - 1)
        self.zoom()

    def zoom_reset(self):
        self._application.save_config(self.ZoomConfigKey, 1)
        self.zoom()

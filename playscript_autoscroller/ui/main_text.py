
from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QFontMetrics,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt5.QtWidgets import (
    QTextEdit,
)


class MainText(QTextEdit):

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

        self._normal_font = self.font()
        self._mono_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self._base_font_size = self.currentFont().pointSize()
        self._zoom_level = self._application.register_config('zoom', self.DefaultZoom)
        self._application.config_restored.connect(self.zoom)

        self.cursorPositionChanged.connect(self.on_cursor_move)
        self.textChanged.connect(application.set_dirty)

    @property
    def content(self):
        return self.toMarkdown(QTextDocument.MarkdownDialectCommonMark)

    @property
    def cursor(self):
        return self._cursor

    @property
    def toolbar(self):
        return self._toolbar

    def go_to_position(self, position):
        cursor = self.textCursor()

        # Jump to the end of the document before going where we want,
        # so that we end up with where we want at the top of the viewport.
        cursor.setPosition(self.document().lastBlock().position())
        self.setTextCursor(cursor)

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

    def on_cursor_move(self):
        char_format = self.currentCharFormat()
        style = {
            "bold": char_format.fontWeight() == QFont.Bold,
            "italic": char_format.fontItalic(),
            "underline": char_format.fontUnderline(),
            "strikethrough": char_format.fontStrikeOut(),
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

        # plaintext pastes only in Source View
        self.setAcceptRichText(not show)

        if show:
            # We have to set the position to 0 before clearing the text formatting, else any
            # text selected before the transition will have its formatting stripped.
            cursor.setPosition(0)
            self.setTextCursor(cursor)

            position *= 1.5
            self.setCurrentCharFormat(QTextCharFormat())
            self.setPlainText(self.toMarkdown(QTextDocument.MarkdownDialectCommonMark))
            self.setFont(self._mono_font)
        else:
            position /= 1.5
            self.setFont(self._normal_font)
            self.setMarkdown(self.toPlainText())
            self.respace_text()

        # Reset to clean if the document content hadn't actually been changed previously
        if not was_dirty:
            self._application.set_clean()

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

    def zoom(self):
        self._normal_font.setPointSize(self._base_font_size + self._zoom_level())
        self._mono_font.setPointSize(self._base_font_size + self._zoom_level())
        if self._application.window.source_view_active:
            self.setFont(self._mono_font)
        else:
            self.setFont(self._normal_font)
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

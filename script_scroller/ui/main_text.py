
from PyQt5.QtGui import (
    QFontMetrics,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt5.QtWidgets import (
    QTextEdit,
)


class MainText(QTextEdit):

    # @todo: Extract these from the active StyleSheet/Theme somehow
    BoldWeight = 75
    NormalWeight = 50

    def __init__(self, application, toolbar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application
        self._toolbar = toolbar

        # According to the CommonMark MarkDown spec, tabs used at the start of a line as
        # indentation should each be replaced with an indent of four spaces.
        # The replacement is done by Qt5, but this also gives a reference for how wide tabs
        # should be.
        fm = QFontMetrics(self.currentFont())
        self.setTabStopDistance(fm.horizontalAdvance(" ") * 4)

        self.respace_text()
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

    def on_cursor_move(self):
        char_format = self.currentCharFormat()
        style = {
            "bold": char_format.fontWeight() == self.BoldWeight,
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
        while block.isValid():
            block_cursor = QTextCursor(block)
            block_format = block.blockFormat()
            block_level = block_format.headingLevel()

            if block_level not in level_spacing:
                char_format = block_cursor.charFormat()
                font = char_format.font()
                level_spacing[block_level] = QFontMetrics(font).height() * 0.8

            block_format.setTopMargin(level_spacing[block_level])
            block_cursor.setBlockFormat(block_format)
            block = block.next()

    def scroll(self, step):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + step)

    def setFontBold(self, checked):
        if checked:
            self.setFontWeight(self.BoldWeight)
        else:
            self.setFontWeight(self.NormalWeight)

    def setFontStrikeThrough(self, checked):
        style = self.currentCharFormat()
        style.setFontStrikeOut(checked)
        self.setCurrentCharFormat(style)

    def show_source_view(self, show):
        # The position multiplication is used to roughly place the cursor back where it was.
        # It's not very accurate, and will get worse the further down a document the cursor is
        # when a transition occurs.
        cursor = self.textCursor()
        position = cursor.position()

        if (show):
            # We have to set the position to 0 before clearing the text formatting, else any
            # text selected before the transition will have its formatting stripped.
            cursor.setPosition(0)
            self.setTextCursor(cursor)

            position *= 1.5
            self.setCurrentCharFormat(QTextCharFormat())
            self.setPlainText(self.toMarkdown(QTextDocument.MarkdownDialectCommonMark))
        else:
            position /= 1.5
            self.setMarkdown(self.toPlainText())
            self.respace_text()

        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

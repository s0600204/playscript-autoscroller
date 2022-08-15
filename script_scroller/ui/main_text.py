
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt5.QtWidgets import (
    QTextEdit,
)

from .main_text_toolbar import MainTextToolbar


class MainText(QTextEdit):

    # @todo: Extract these from the active StyleSheet/Theme somehow
    BoldWeight = 75
    NormalWeight = 50

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application
        self._toolbar = MainTextToolbar(self)

        self.cursorPositionChanged.connect(self.on_cursor_move)

    @property
    def cursor(self):
        return self._cursor

    @property
    def toolbar(self):
        return self._toolbar

    def on_cursor_move(self):
        self._toolbar._action_bold.setChecked(self.fontWeight() == self.BoldWeight)
        self._toolbar._action_italic.setChecked(self.fontItalic())
        self._toolbar._action_underline.setChecked(self.fontUnderline())

        style = self.currentCharFormat()
        self._toolbar._action_strikethrough.setChecked(style.fontStrikeOut())

    def retranslate_ui(self):
        self._toolbar.retranslate_ui()

    def scroll(self, step):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + step)

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
            self.setPlainText(self.toMarkdown())
            self._toolbar.set_text_formatting_enabled(False)
        else:
            position /= 1.5
            self.setMarkdown(self.toPlainText())
            self._toolbar.set_text_formatting_enabled(True)

        cursor = self.textCursor()
        cursor.setPosition(int(position))
        self.setTextCursor(cursor)

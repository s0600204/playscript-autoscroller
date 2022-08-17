
from os import path

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QToolBar,
)


class MainToolbar(QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFloatable(False)
        self.setMovable(False)

        self._action_bold = QAction(parent=self)
        self._action_bold.setCheckable(True)
        self._action_bold.setIcon(
            QIcon.fromTheme(
                'format-text-bold',
                QIcon.fromTheme('format-text-bold-symbolic')))

        self._action_italic = QAction(parent=self)
        self._action_italic.setCheckable(True)
        self._action_italic.setIcon(
            QIcon.fromTheme(
                'format-text-italic',
                QIcon.fromTheme('format-text-italic-symbolic')))

        self._action_underline = QAction(parent=self)
        self._action_underline.setCheckable(True)
        self._action_underline.setIcon(
            QIcon.fromTheme(
                'format-text-underline',
                QIcon.fromTheme('format-text-underline-symbolic')))

        self._action_strikethrough = QAction(parent=self)
        self._action_strikethrough.setCheckable(True)
        self._action_strikethrough.setIcon(
            QIcon.fromTheme(
                'format-text-strikethrough',
                QIcon.fromTheme('format-text-strikethrough-symbolic')))

        self._action_source_view = QAction(parent=self)
        self._action_source_view.setCheckable(True)
        self._action_source_view.setIcon(
            QIcon(
                f"{path.dirname(__file__)}/icons/view-source.svg"))

        self.addAction(self._action_bold)
        self.addAction(self._action_italic)
        #self.addAction(self._action_underline) # MarkDown doesn't support underlined text
        self.addAction(self._action_strikethrough)
        self.addSeparator()
        self.addAction(self._action_source_view)

    def connect_textfield(self, textfield):
        self._action_bold.triggered.connect(textfield.setFontBold)
        self._action_italic.triggered.connect(textfield.setFontItalic)
        self._action_underline.triggered.connect(textfield.setFontUnderline)
        self._action_strikethrough.triggered.connect(textfield.setFontStrikeThrough)
        self._action_source_view.triggered.connect(self.parent().show_source_view)

    def set_text_formatting_enabled(self, enabled):
        # It might be nice to not disable the buttons in "source view", but instead add/remove
        # the appropriate character strings around the selected text.
        self._action_bold.setEnabled(enabled)
        self._action_italic.setEnabled(enabled)
        self._action_underline.setEnabled(enabled)
        self._action_strikethrough.setEnabled(enabled)

    def retranslate_ui(self):
        self._action_bold.setText("Bold")
        self._action_bold.setShortcut(QKeySequence.Bold)

        self._action_italic.setText("Italic")
        self._action_italic.setShortcut(QKeySequence.Italic)

        self._action_underline.setText("Underline")
        self._action_underline.setShortcut(QKeySequence.Underline)

        self._action_strikethrough.setText("Strikethrough")

        self._action_source_view.setText("View Source")

    def update_style_buttons(self, style):
        self._action_bold.setChecked(style["bold"])
        self._action_italic.setChecked(style["italic"])
        self._action_underline.setChecked(style["underline"])
        self._action_strikethrough.setChecked(style["strikethrough"])

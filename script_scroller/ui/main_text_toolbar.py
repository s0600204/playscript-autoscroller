
from os import path

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QToolBar,
)


class MainTextToolbar(QToolBar):

    def __init__(self, textfield, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._textfield = textfield

        self.setFloatable(False)
        self.setMovable(False)


        self._action_bold = QAction(parent=self)
        self._action_bold.setCheckable(True)
        self._action_bold.setIcon(
            QIcon.fromTheme(
                'format-text-bold',
                QIcon.fromTheme('format-text-bold-symbolic')))
        self._action_bold.triggered.connect(self.on_bold_action)

        self._action_italic = QAction(parent=self)
        self._action_italic.setCheckable(True)
        self._action_italic.setIcon(
            QIcon.fromTheme(
                'format-text-italic',
                QIcon.fromTheme('format-text-italic-symbolic')))
        self._action_italic.triggered.connect(self._textfield.setFontItalic)

        self._action_underline = QAction(parent=self)
        self._action_underline.setCheckable(True)
        self._action_underline.setIcon(
            QIcon.fromTheme(
                'format-text-underline',
                QIcon.fromTheme('format-text-underline-symbolic')))
        self._action_underline.triggered.connect(self._textfield.setFontUnderline)

        self._action_strikethrough = QAction(parent=self)
        self._action_strikethrough.setCheckable(True)
        self._action_strikethrough.setIcon(
            QIcon.fromTheme(
                'format-text-strikethrough',
                QIcon.fromTheme('format-text-strikethrough-symbolic')))
        self._action_strikethrough.triggered.connect(self.on_strikethrough_action)

        self._action_source_view = QAction(parent=self)
        self._action_source_view.setCheckable(True)
        self._action_source_view.setIcon(
            QIcon(
                f"{path.dirname(__file__)}/icons/view-source.svg"))
        self._action_source_view.triggered.connect(textfield.show_source_view)

        self.addAction(self._action_bold)
        self.addAction(self._action_italic)
        self.addAction(self._action_underline)
        self.addAction(self._action_strikethrough)
        self.addSeparator()
        self.addAction(self._action_source_view)

    def set_text_formatting_enabled(self, enabled):
        # It might be nice to not disable the buttons in "source view", but instead add/remove
        # the appropriate character strings around the selected text.
        self._action_bold.setEnabled(enabled)
        self._action_italic.setEnabled(enabled)
        self._action_underline.setEnabled(enabled)
        self._action_strikethrough.setEnabled(enabled)

    def on_bold_action(self, checked):
        if checked:
            self._textfield.setFontWeight(self._textfield.BoldWeight)
        else:
            self._textfield.setFontWeight(self._textfield.NormalWeight)

    def on_strikethrough_action(self, checked):
        style = self._textfield.currentCharFormat()
        style.setFontStrikeOut(checked)
        self._textfield.setCurrentCharFormat(style)

    def retranslate_ui(self):
        self._action_bold.setText("Bold")
        self._action_bold.setShortcut(QKeySequence.Bold)

        self._action_italic.setText("Italic")
        self._action_italic.setShortcut(QKeySequence.Italic)

        self._action_underline.setText("Underline")
        self._action_underline.setShortcut(QKeySequence.Underline)

        self._action_strikethrough.setText("Strikethrough")

        self._action_source_view.setText("View Source")

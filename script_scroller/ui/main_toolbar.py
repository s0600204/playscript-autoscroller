
from os import path

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QToolBar

from .toolbar_action import ToolbarAction


class MainToolbar(QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFloatable(False)
        self.setMovable(False)

        self._action_outline = ToolbarAction(parent=self)
        self._action_outline.setCheckable(True)
        self._action_outline.setChecked(True)
        self._action_outline.set_icon('sidebar-show', 'sidebar-open', 'sidebar-close')

        self._action_bold = ToolbarAction(parent=self)
        self._action_bold.setCheckable(True)
        self._action_bold.set_icon('format-text-bold')

        self._action_italic = ToolbarAction(parent=self)
        self._action_italic.setCheckable(True)
        self._action_italic.set_icon('format-text-italic')

        self._action_underline = ToolbarAction(parent=self)
        self._action_underline.setCheckable(True)
        self._action_underline.set_icon('format-text-underline')

        self._action_strikethrough = ToolbarAction(parent=self)
        self._action_strikethrough.setCheckable(True)
        self._action_strikethrough.set_icon('format-text-strikethrough')

        self._action_zoom_in = ToolbarAction(parent=self)
        self._action_zoom_in.set_icon('zoom-in')

        self._action_zoom_out = ToolbarAction(parent=self)
        self._action_zoom_out.set_icon('zoom-out')

        self._action_zoom_reset = ToolbarAction(parent=self)
        self._action_zoom_reset.set_icon('zoom-original')

        self._action_source_view = ToolbarAction(parent=self)
        self._action_source_view.setCheckable(True)
        self._action_source_view.set_icon('text-x-source', 'file-code')

        self.addAction(self._action_outline)
        self.addSeparator()
        self.addAction(self._action_bold)
        self.addAction(self._action_italic)
        #self.addAction(self._action_underline) # MarkDown doesn't support underlined text
        self.addAction(self._action_strikethrough)
        self.addSeparator()
        self.addAction(self._action_zoom_in)
        self.addAction(self._action_zoom_out)
        self.addAction(self._action_zoom_reset)
        self.addSeparator()
        self.addAction(self._action_source_view)

    def connect_textfield(self, textfield):
        self._action_outline.triggered.connect(self.parent().show_outline)
        self._action_bold.triggered.connect(textfield.setFontBold)
        self._action_italic.triggered.connect(textfield.setFontItalic)
        self._action_underline.triggered.connect(textfield.setFontUnderline)
        self._action_strikethrough.triggered.connect(textfield.setFontStrikeThrough)
        self._action_zoom_in.triggered.connect(textfield.zoom_in)
        self._action_zoom_out.triggered.connect(textfield.zoom_out)
        self._action_zoom_reset.triggered.connect(textfield.zoom_reset)
        self._action_source_view.triggered.connect(self.parent().show_source_view)

    def set_source_view_checked(self, checked):
        self._action_source_view.setChecked(checked)

    def set_text_formatting_enabled(self, enabled):
        self._action_outline.setEnabled(enabled)
        # It might be nice to not disable the buttons in "source view", but instead add/remove
        # the appropriate character strings around the selected text.
        self._action_bold.setEnabled(enabled)
        self._action_italic.setEnabled(enabled)
        self._action_underline.setEnabled(enabled)
        self._action_strikethrough.setEnabled(enabled)

    def retranslate_ui(self):
        self._action_outline.setText("Toggle Outline")

        self._action_bold.setText("Bold")
        self._action_bold.setShortcut(QKeySequence.Bold)

        self._action_italic.setText("Italic")
        self._action_italic.setShortcut(QKeySequence.Italic)

        self._action_underline.setText("Underline")
        self._action_underline.setShortcut(QKeySequence.Underline)

        self._action_strikethrough.setText("Strikethrough")

        self._action_zoom_in.setText("Zoom In")
        self._action_zoom_out.setText("Zoom Out")
        self._action_zoom_reset.setText("Zoom Reset")

        self._action_source_view.setText("View Source")

    def should_show_outline(self):
        return self._action_outline.isChecked()

    def update_style_buttons(self, style):
        self._action_bold.setChecked(style["bold"])
        self._action_italic.setChecked(style["italic"])
        self._action_underline.setChecked(style["underline"])
        self._action_strikethrough.setChecked(style["strikethrough"])

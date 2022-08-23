
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QToolBar

from .toolbar_action import ToolbarAction


class MainToolbar(QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFloatable(False)
        self.setMovable(False)

        self._textfield = None
        self._actions = {}

        self._actions["outline"] = ToolbarAction(parent=self)
        self._actions["outline"].setCheckable(True)
        self._actions["outline"].setChecked(True)
        self._actions["outline"].set_icon('sidebar-show', 'sidebar-open', 'sidebar-close')

        self._actions["bold"] = ToolbarAction(parent=self)
        self._actions["bold"].setCheckable(True)
        self._actions["bold"].set_icon('format-text-bold')

        self._actions["italic"] = ToolbarAction(parent=self)
        self._actions["italic"].setCheckable(True)
        self._actions["italic"].set_icon('format-text-italic')

        self._actions["underline"] = ToolbarAction(parent=self)
        self._actions["underline"].setCheckable(True)
        self._actions["underline"].set_icon('format-text-underline')

        self._actions["strikethrough"] = ToolbarAction(parent=self)
        self._actions["strikethrough"].setCheckable(True)
        self._actions["strikethrough"].set_icon('format-text-strikethrough')

        self._actions["dedent"] = ToolbarAction(parent=self)
        self._actions["dedent"].setEnabled(False)
        self._actions["dedent"].set_icon('format-indent-less', 'outdent')
        self._actions["dedent"].triggered.connect(self.dedent)

        self._actions["indent"] = ToolbarAction(parent=self)
        self._actions["indent"].set_icon('format-indent-more', 'indent')
        self._actions["indent"].triggered.connect(self.indent)

        self._actions["zoom_in"] = ToolbarAction(parent=self)
        self._actions["zoom_in"].set_icon('zoom-in')

        self._actions["zoom_out"] = ToolbarAction(parent=self)
        self._actions["zoom_out"].set_icon('zoom-out')

        self._actions["zoom_reset"] = ToolbarAction(parent=self)
        self._actions["zoom_reset"].set_icon('zoom-original')

        self._actions["source_view"] = ToolbarAction(parent=self)
        self._actions["source_view"].setCheckable(True)
        self._actions["source_view"].set_icon('text-x-source', 'file-code')

        self.addAction(self._actions["outline"])
        self.addSeparator()
        self.addAction(self._actions["bold"])
        self.addAction(self._actions["italic"])
        self.addAction(self._actions["underline"])
        self.addAction(self._actions["strikethrough"])
        self.addSeparator()
        self.addAction(self._actions["dedent"])
        self.addAction(self._actions["indent"])
        self.addSeparator()
        self.addAction(self._actions["zoom_in"])
        self.addAction(self._actions["zoom_out"])
        self.addAction(self._actions["zoom_reset"])
        self.addSeparator()
        self.addAction(self._actions["source_view"])

    def connect_textfield(self, textfield):
        self._textfield = textfield
        self._actions["outline"].triggered.connect(self.parent().show_outline)
        self._actions["outline"].enabled.connect(self.parent().enable_outline)
        self._actions["bold"].triggered.connect(textfield.setFontBold)
        self._actions["italic"].triggered.connect(textfield.setFontItalic)
        self._actions["underline"].triggered.connect(textfield.setFontUnderline)
        self._actions["strikethrough"].triggered.connect(textfield.setFontStrikeThrough)
        self._actions["zoom_in"].triggered.connect(self.parent().zoom_in)
        self._actions["zoom_out"].triggered.connect(self.parent().zoom_out)
        self._actions["zoom_reset"].triggered.connect(self.parent().zoom_reset)
        self._actions["source_view"].triggered.connect(self.parent().show_source_view)

    def dedent(self):
        if self._textfield:
            indent = self._textfield.dedent()
            self._actions["dedent"].setEnabled(indent)

    def indent(self):
        if self._textfield:
            self._textfield.indent()
            self._actions["dedent"].setEnabled(True)

    def set_source_view_checked(self, checked):
        self._actions["source_view"].setChecked(checked)

    def retranslate_ui(self):
        self._actions["outline"].setText("Toggle Outline")

        self._actions["bold"].setText("Bold")
        self._actions["bold"].setShortcut(QKeySequence.Bold)

        self._actions["italic"].setText("Italic")
        self._actions["italic"].setShortcut(QKeySequence.Italic)

        self._actions["underline"].setText("Underline")
        self._actions["underline"].setShortcut(QKeySequence.Underline)

        self._actions["strikethrough"].setText("Strikethrough")

        self._actions["dedent"].setText("Decrease Indent")
        self._actions["indent"].setText("Increase Indent")

        self._actions["zoom_in"].setText("Zoom In")
        self._actions["zoom_out"].setText("Zoom Out")
        self._actions["zoom_reset"].setText("Zoom Reset")

        self._actions["source_view"].setText("View Source")

    def should_show_outline(self):
        return self._actions["outline"].isChecked()

    def update_enabled_buttons(self):
        pdf_view_active = self.parent().pdf_view_active
        source_view_active = self.parent().source_view_active
        toc_active = self.parent().toc_active

        if source_view_active:
            self._actions["outline"].setEnabled(False)
        elif pdf_view_active:
            self._actions["outline"].setEnabled(toc_active)
        else:
            self._actions["outline"].setEnabled(True)

        # It might be nice to not disable the buttons in "source view", but instead add/remove
        # the appropriate character strings around the selected text.
        self._actions["bold"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["italic"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["underline"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["strikethrough"].setEnabled(not pdf_view_active and not source_view_active)

        # Dedent starts "off" even in non-pdf mode, as the cursor is at the start of a line.
        self._actions["dedent"].setEnabled(False)
        self._actions["indent"].setEnabled(not pdf_view_active)

        self._actions["zoom_in"].setEnabled(True)
        self._actions["zoom_out"].setEnabled(True)
        self._actions["zoom_reset"].setEnabled(True)

        self._actions["source_view"].setEnabled(not pdf_view_active)

    def update_source_view_checked(self):
        self._actions["source_view"].setChecked(self.parent().source_view_active)

    def update_style_buttons(self, style):
        self._actions["bold"].setChecked(style["bold"])
        self._actions["italic"].setChecked(style["italic"])
        self._actions["underline"].setChecked(style["underline"])
        self._actions["strikethrough"].setChecked(style["strikethrough"])
        self._actions["dedent"].setEnabled(style["indent"])

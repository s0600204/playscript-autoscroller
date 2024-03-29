
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QToolBar

from .action_classes import ToolbarAction, ToolButtonAction
from .menus.heading_submenu import HeadingSubMenu


class MainToolbar(QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFloatable(False)
        self.setMovable(False)

        self._textfield = None
        self._actions = {}

        self._actions["outline"] = ToolbarAction(self)
        self._actions["outline"].setCheckable(True)
        self._actions["outline"].setChecked(True)
        self._actions["outline"].set_icon('sidebar-open', 'sidebar-close')

        self._actions["heading"] = ToolButtonAction(self)
        self._actions["heading"].set_icon('heading')
        self._actions["heading"].setPopupMode(ToolButtonAction.InstantPopup)
        self._actions["heading"].setMenu(HeadingSubMenu(parent=self._actions["heading"]))

        self._actions["bold"] = ToolbarAction(self)
        self._actions["bold"].setCheckable(True)
        self._actions["bold"].set_icon('bold')

        self._actions["italic"] = ToolbarAction(self)
        self._actions["italic"].setCheckable(True)
        self._actions["italic"].set_icon('italic')

        self._actions["underline"] = ToolbarAction(self)
        self._actions["underline"].setCheckable(True)
        self._actions["underline"].set_icon('underline')

        self._actions["strikethrough"] = ToolbarAction(self)
        self._actions["strikethrough"].setCheckable(True)
        self._actions["strikethrough"].set_icon('strikethrough')

        self._actions["monospace"] = ToolbarAction(self)
        self._actions["monospace"].setCheckable(True)
        self._actions["monospace"].set_icon('code')

        self._actions["clear_format"] = ToolbarAction(self)
        self._actions["clear_format"].setCheckable(False)
        self._actions["clear_format"].set_icon('clear-format')

        self._actions["dedent"] = ToolbarAction(self)
        self._actions["dedent"].setEnabled(False)
        self._actions["dedent"].set_icon('outdent')
        self._actions["dedent"].triggered.connect(self.dedent)

        self._actions["indent"] = ToolbarAction(self)
        self._actions["indent"].set_icon('indent')
        self._actions["indent"].triggered.connect(self.indent)

        self._actions["zoom_in"] = ToolbarAction(self)
        self._actions["zoom_in"].set_icon('zoom-in')

        self._actions["zoom_out"] = ToolbarAction(self)
        self._actions["zoom_out"].set_icon('zoom-out')

        self._actions["zoom_reset"] = ToolbarAction(self)
        self._actions["zoom_reset"].set_icon('zoom-reset')

        self._actions["source_view"] = ToolbarAction(self)
        self._actions["source_view"].setCheckable(True)
        self._actions["source_view"].set_icon('file-code')

        self.addAction(self._actions["outline"])
        self.addSeparator()
        self.addWidget(self._actions["heading"])
        self.addSeparator()
        self.addAction(self._actions["bold"])
        self.addAction(self._actions["italic"])
        self.addAction(self._actions["underline"])
        self.addAction(self._actions["strikethrough"])
        self.addAction(self._actions["monospace"])
        self.addAction(self._actions["clear_format"])
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
        self._actions["heading"].menu().connect_textfield(textfield)
        self._actions["bold"].triggered.connect(textfield.setFontBold)
        self._actions["italic"].triggered.connect(textfield.setFontItalic)
        self._actions["underline"].triggered.connect(textfield.setFontUnderline)
        self._actions["strikethrough"].triggered.connect(textfield.setFontStrikeThrough)
        self._actions["monospace"].triggered.connect(textfield.setFontMonospace)
        self._actions["clear_format"].triggered.connect(textfield.clear_format)
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

        self._actions["heading"].setText("Heading Level")
        self._actions["heading"].menu().retranslate_ui()

        self._actions["bold"].setText("Bold")
        self._actions["bold"].setShortcut(QKeySequence.Bold)

        self._actions["italic"].setText("Italic")
        self._actions["italic"].setShortcut(QKeySequence.Italic)

        self._actions["underline"].setText("Underline")
        self._actions["underline"].setShortcut(QKeySequence.Underline)

        self._actions["strikethrough"].setText("Strikethrough")

        self._actions["monospace"].setText("Monospace")

        self._actions["clear_format"].setText("Clear Character Formatting")

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
        self._actions["heading"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["bold"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["italic"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["underline"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["strikethrough"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["monospace"].setEnabled(not pdf_view_active and not source_view_active)
        self._actions["clear_format"].setEnabled(not pdf_view_active and not source_view_active)

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
        self._actions["heading"].menu().update_style_buttons(style)
        self._actions["bold"].setChecked(style["bold"])
        self._actions["italic"].setChecked(style["italic"])
        self._actions["underline"].setChecked(style["underline"])
        self._actions["strikethrough"].setChecked(style["strikethrough"])
        self._actions["monospace"].setChecked(style["monospace"])
        self._actions["dedent"].setEnabled(style["indent"])

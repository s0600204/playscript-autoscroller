
from qtpy.QtWidgets import QMenu

from ..action_classes import MenuAction


class HeadingSubMenu(QMenu):

    HeadingLevels = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions = {}

        for level in range(1, self.HeadingLevels + 1):
            key = f"heading_{level}"
            self._actions[key] = MenuAction(parent=self)
            self._actions[key].setCheckable(True)
            self.addAction(self._actions[f"heading_{level}"])

    def build_heading_closure(self, textfield, level):
        def _set_heading(checked):
            textfield.setTextHeadingLevel(checked and level or 0)
        return _set_heading

    def connect_textfield(self, textfield):
        for level in range(1, self.HeadingLevels + 1):
            self._actions[f"heading_{level}"].triggered.connect(
                self.build_heading_closure(textfield, level))

    def retranslate_ui(self):
        for level in range(1, self.HeadingLevels + 1):
            self._actions[f"heading_{level}"].setText(f"Heading Level {level}")
            if level == 1:
                tip = "Set Heading Level 1 (Largest)"
            elif level == self.HeadingLevels:
                tip = f"Set Heading Level {self.HeadingLevels} (Smallest)"
            else:
                tip = f"Set Heading Level {level}"
            self._actions[f"heading_{level}"].setStatusTip(tip)

    def update_style_buttons(self, style):
        if style["heading_level"] == 0:
            self.parent().set_icon("heading")
        else:
            self.parent().set_icon(f"heading-{style['heading_level']}")
        for level in range(1, self.HeadingLevels + 1):
            self._actions[f"heading_{level}"].setChecked(style["heading_level"] == level)

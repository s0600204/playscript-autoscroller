
from os import path

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QIcon
from qtpy.QtWidgets import (
    QGridLayout,
    QProgressBar,
    QPushButton,
    QSlider,
    QWidget,
)

from .palette_icon_engine import PaletteIconEngine


class Controller(QWidget):

    Default = 63

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._application = application
        self._config_getter = self._application.register_config('midpoint', self.Default)
        self._cached_value = (0, 100)

        self.setLayout(QGridLayout())

        self._status = QProgressBar(self)
        self._status.setRange(0, 127)
        self._status.setTextVisible(False)
        self.layout().addWidget(self._status, 0, 0)

        self._midpoint = QSlider(Qt.Horizontal, self)
        self._midpoint.setMinimum(0)
        self._midpoint.setMaximum(127)
        self._midpoint.setTickPosition(QSlider.TicksAbove)
        self.layout().addWidget(self._midpoint, 1, 0)

        button_style = f"\
            * {{ \
                color: { self.palette().windowText().color().name(QColor.HexArgb) }; \
            }} \
            *:checked {{ \
                background-color: #f70000; \
                color: { self.palette().windowText().color().name(QColor.HexArgb) }; \
            }}"

        _ignore_icon = QIcon(PaletteIconEngine(self.palette))
        _ignore_icon.addFile(path.join(path.dirname(__file__), './icons/lucide/x.svg'))
        self._ignore_button = QPushButton(self)
        self._ignore_button.setCheckable(True)
        self._ignore_button.setChecked(False)
        self._ignore_button.setIcon(_ignore_icon)
        self._ignore_button.setStyleSheet(button_style)
        self._ignore_button.pressed.connect(self.on_ignore)
        self.layout().addWidget(self._ignore_button, 0, 1)

        _pause_icon = QIcon(PaletteIconEngine(self.palette))
        _pause_icon.addFile(path.join(path.dirname(__file__), './icons/lucide/pause.svg'))
        self._pause_button = QPushButton(self)
        self._pause_button.setCheckable(True)
        self._pause_button.setChecked(True)
        self._pause_button.setIcon(_pause_icon)
        self._pause_button.setStyleSheet(button_style)
        self.layout().addWidget(self._pause_button, 1, 1)

        # Default position
        self.midpoint = self.Default

        self._application.config_restored.connect(self.deserialise)
        self._midpoint.valueChanged.connect(self.serialise)

        runner = self._application.runner
        runner.ignoreToggled.connect(self.toggle_ignore)
        runner.midpointUpdate.connect(self.update_midpoint)
        runner.pauseToggled.connect(self.toggle_pause)
        runner.scrollUpdate.connect(self.update_scroll)

    @property
    def midpoint(self):
        """Value that is the midpoint of the input."""
        return self._midpoint.value()

    @midpoint.setter
    def midpoint(self, new_midpoint):
        self._midpoint.setValue(new_midpoint)
        self._status.setValue(new_midpoint)

    def on_ignore(self):
        self._status.setEnabled(
            self._ignore_button.isChecked())

    def serialise(self, new_midpoint):
        self._application.save_config('midpoint', new_midpoint)

    def deserialise(self):
        self.midpoint = self._config_getter()

    def retranslate_ui(self):
        self._ignore_button.setText('I&gnore')
        self._ignore_button.setToolTip('Ignore input from MIDI device')
        self._ignore_button.setShortcut('Ctrl+G')

        self._pause_button.setText('&Pause')
        self._pause_button.setToolTip('Pause scrolling')
        self._pause_button.setShortcut('Ctrl+P')

    def toggle_ignore(self):
        self._ignore_button.setChecked(
            not self._ignore_button.isChecked())

    def toggle_pause(self):
        self._pause_button.setChecked(
            not self._pause_button.isChecked())

    def update_midpoint(self, new_value):
        self._midpoint.setValue(new_value)

    def update_scroll(self, new_value):
        if self._ignore_button.isChecked():
            return
        self._status.setValue(new_value)

    def value(self):

        if self._pause_button.isChecked():
            return (0, 100)

        if self._ignore_button.isChecked():
            return self._cached_value

        diff = self._status.value() - self._midpoint.value()
        self._cached_value = (
            round(diff / 6),
            round(1000 / (abs(diff / 2) + 10))
        )
        return self._cached_value

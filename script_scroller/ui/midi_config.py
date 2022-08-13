
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QSpinBox,
)

from .device_selector import DeviceSelector


class MidiConfigDialog(QDialog):

    Defaults = {
        'device': '',
        'channel': 1,
        'control': 7,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(QFormLayout())

        self._device_label = QLabel(self)
        self._device_selector = DeviceSelector(self)
        self._device_selector.refresh()
        if self._device_selector.count():
            self._device_selector.setCurrentIndex(1)
        self.layout().addRow(self._device_label, self._device_selector)

        self._channel_label = QLabel(self)
        self._channel_selector = QSpinBox(self)
        self._channel_selector.setRange(1, 16)
        self._channel_selector.setValue(self.Defaults['channel'])
        self.layout().addRow(self._channel_label, self._channel_selector)

        self._control_label = QLabel(self)
        self._control_selector = QSpinBox(self)
        self._control_selector.setRange(0, 127)
        self._control_selector.setValue(self.Defaults['control'])
        self.layout().addRow(self._control_label, self._control_selector)

        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(QDialogButtonBox.Save)
        self._button_box.addButton(QDialogButtonBox.Cancel)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
        self.layout().addRow(self._button_box)

        self.retranslate_ui()

    def deserialise(self, config):
        self._device_selector.setValue(config['device'])
        self._channel_selector.setValue(config['channel'])
        self._control_selector.setValue(config['control'])

    def retranslate_ui(self):
        self._device_label.setText('MIDI Device')
        self._channel_label.setText('MIDI Channel')
        self._control_label.setText('Control #')

    def serialise(self):
        return {
            'device': self._device_selector.value(),
            'channel': self._channel_selector.value(),
            'control': self._control_selector.value(),
        }

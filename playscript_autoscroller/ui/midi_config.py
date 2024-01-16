
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
)

from .device_selector import DeviceSelector


class MidiConfigDialog(QDialog):

    Defaults = {
        'device': '',
        'channel': 1,
        'scroll_control': 7,
        'midpoint_control': 8,
        'ignore_note': 0,
        'pause_note': 2,
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

        # Scroller control
        self._scroller_group = QGroupBox(self)
        self._scroller_group.setLayout(QFormLayout())
        self.layout().addRow(self._scroller_group)

        self._control_label = QLabel(self)
        self._control_selector = QSpinBox(self)
        # CC 120 - 127 are Channel Mode Messages; and shouldn't be used arbitrarily.
        self._control_selector.setRange(0, 119)
        self._control_selector.setValue(self.Defaults['scroll_control'])
        self._scroller_group.layout().addRow(self._control_label, self._control_selector)

        self._midpoint_label = QLabel(self)
        self._midpoint_selector = QSpinBox(self)
        self._midpoint_selector.setRange(0, 119)
        self._midpoint_selector.setValue(self.Defaults['midpoint_control'])
        self._scroller_group.layout().addRow(self._midpoint_label, self._midpoint_selector)

        # "Ignore" button
        self._ignore_group = QGroupBox(self)
        self._ignore_group.setLayout(QFormLayout())
        self.layout().addRow(self._ignore_group)

        self._ignore_type_label = QLabel(self)
        self._ignore_type_selector = QComboBox(self)
        self._ignore_type_selector.addItem('-')
        self._ignore_type_selector.setDisabled(True)
        self._ignore_group.layout().addRow(self._ignore_type_label, self._ignore_type_selector)

        self._ignore_value_label = QLabel(self)
        self._ignore_value_selector = QSpinBox(self)
        self._ignore_value_selector.setRange(0, 127)
        self._ignore_value_selector.setValue(self.Defaults['ignore_note'])
        self._ignore_group.layout().addRow(self._ignore_value_label, self._ignore_value_selector)

        # "Pause" button
        self._pause_group = QGroupBox(self)
        self._pause_group.setLayout(QFormLayout())
        self.layout().addRow(self._pause_group)

        self._pause_type_label = QLabel(self)
        self._pause_type_selector = QComboBox(self)
        self._pause_type_selector.addItem('-')
        self._pause_type_selector.setDisabled(True)
        self._pause_group.layout().addRow(self._pause_type_label, self._pause_type_selector)

        self._pause_value_label = QLabel(self)
        self._pause_value_selector = QSpinBox(self)
        self._pause_value_selector.setRange(0, 127)
        self._pause_value_selector.setValue(self.Defaults['pause_note'])
        self._pause_group.layout().addRow(self._pause_value_label, self._pause_value_selector)

        # Save / Cancel Buttons
        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(QDialogButtonBox.Save)
        self._button_box.addButton(QDialogButtonBox.Cancel)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
        self.layout().addRow(self._button_box)

        self.retranslate_ui()

    def conform_sizes(self):
        # Conform all nested controls to the same spacing
        labels = [
            self._control_label,
            self._midpoint_label,
            self._ignore_type_label,
            self._ignore_value_label,
            self._pause_type_label,
            self._pause_value_label,
        ]
        width = 0
        for label in labels:
            width = max(label.sizeHint().width(), width)
        for label in labels:
            label.setMinimumWidth(width)

    def deserialise(self, config):
        self._device_selector.setValue(config['device'])
        self._channel_selector.setValue(config['channel'] + 1)
        self._control_selector.setValue(config['scroll_control'])
        self._midpoint_selector.setValue(config['midpoint_control'])
        self._ignore_value_selector.setValue(config['ignore_note'])
        self._pause_value_selector.setValue(config['pause_note'])

    def retranslate_ui(self):
        self._device_label.setText('MIDI Device')
        self._device_selector.setPlaceholderText('Select...')
        self._channel_label.setText('MIDI Channel')

        self._scroller_group.setTitle('Scrolling')
        self._control_label.setText('Scrolling Control #')
        self._midpoint_label.setText('Midpoint Control #')

        self._pause_group.setTitle('Pause Button')
        self._pause_type_label.setText('Message Type')
        self._pause_type_selector.setItemText(0, 'Note On')
        self._pause_value_label.setText('Note #')

        self._ignore_group.setTitle('Ignore Button')
        self._ignore_type_label.setText('Message Type')
        self._ignore_type_selector.setItemText(0, 'Note On')
        self._ignore_value_label.setText('Note #')

        self.conform_sizes()

    def serialise(self):
        return {
            'device': self._device_selector.value() or '',
            'channel': self._channel_selector.value() - 1,
            'scroll_control': self._control_selector.value(),
            'midpoint_control': self._midpoint_selector.value(),
            'ignore_note': self._ignore_value_selector.value(),
            'pause_note': self._pause_value_selector.value(),
        }

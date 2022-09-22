
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QComboBox

from playscript_autoscroller.midi_devices import MidiDevices


class DeviceSelector(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_list = MidiDevices()

    def add_subheader(self, caption):
        new_item = QStandardItem(caption)
        new_item.setEnabled(False)
        font = new_item.font()
        font.setBold(True)
        new_item.setFont(font)
        self.model().appendRow(new_item)

    def refresh(self):
        self.device_list.refresh()
        self.clear()

        for dev in self.device_list.devices():
            self.add_subheader(dev.ui_name)
            for port in dev.in_ports:
                self.addItem(port.ui_name, port.mido_name)

    def setValue(self, new_value):
        # pylint: disable=invalid-name
        idx = self.findData(new_value)
        self.setCurrentIndex(idx)

    def value(self):
        return self.itemData(self.currentIndex())

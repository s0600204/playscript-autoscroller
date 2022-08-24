
import mido

from PyQt5.QtCore import pyqtSignal, QObject

from .ui.midi_config import MidiConfigDialog


class MidiRunner(QObject):

    ConfigKey = 'midi'
    ValueReceived = pyqtSignal(int, name='valueReceived')

    def __init__(self, application):
        super().__init__()
        self._application = application
        self._port = None

        self._config_dialog = None
        self._config_getter = self._application.register_config(
            self.ConfigKey, MidiConfigDialog.Defaults)
        self._config = self._config_getter()

        self._application.config_restored.connect(self.restore_from_config)

    def on_midi_message(self, message):
        if not message.is_cc() \
            or message.channel != self._config['channel'] \
            or message.control != self._config['control']:
            return
        self.ValueReceived.emit(message.value)

    def restore_from_config(self):
        self._config = self._config_getter()
        self.start()

    def on_config_change(self):
        last_device = self._config['device']
        self._application.save_config(self.ConfigKey, self._config_dialog.serialise())
        self._config = self._config_getter()
        if self._config['device'] != last_device:
            self.stop()
            self.start()

    def open_config_dialog(self, ui_parent):
        if not self._config_dialog:
            self._config_dialog = MidiConfigDialog(parent=ui_parent)
            self._config_dialog.accepted.connect(self.on_config_change)

        self._config_dialog.deserialise(self._config)
        self._config_dialog.show()

    def start(self):
        try:
            self._port = mido.open_input(self._config['device'])
        except IOError:
            self._application.window.show_status_message(
                "MIDI Device not connected!")
            return

        self._port.callback = self.on_midi_message
        self._application.window.show_status_message(
            "Started MIDI Runner")

    def stop(self):
        if self._port:
            self._port.callback = None
            self._port.close()
            self._application.window.show_status_message(
                "Stopped MIDI Runner")

    def shutdown(self):
        self.stop()

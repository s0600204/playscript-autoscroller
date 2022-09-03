
import mido

from PyQt5.QtCore import pyqtSignal, QObject

from .ui.midi_config import MidiConfigDialog


class MidiRunner(QObject):

    ConfigKey = 'midi'
    ScrollUpdate = pyqtSignal(int, name='scrollUpdate')
    MidpointUpdate = pyqtSignal(int, name='midpointUpdate')
    PauseToggled = pyqtSignal(name='pauseToggled')
    IgnoreToggled = pyqtSignal(name='ignoreToggled')

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
        if message.channel != self._config['channel']:
            return

        if message.type == 'control_change':
            if message.control == self._config['scroll_control']:
                self.ScrollUpdate.emit(message.value)
            elif message.control == self._config['midpoint_control']:
                self.MidpointUpdate.emit(message.value)
            return

        if message.type == 'note_on':
            if message.note == self._config['ignore_note']:
                self.IgnoreToggled.emit()
            elif message.note == self._config['pause_note']:
                self.PauseToggled.emit()

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

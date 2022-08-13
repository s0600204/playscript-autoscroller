
from PyQt5.QtCore import pyqtSignal, QObject

from .file_io import (
    load_config_file,
    save_config_file,
)
from .ui.main_window import MainWindow


class Application(QObject):

    config_restored = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._config = None

        self._mainwindow = MainWindow(self)

        self.load_config()

    def load_config(self):
        config = load_config_file()
        if not config:
            self._mainwindow.show_status_message(
                "No valid configuration found")
            return

        self._config = config
        self._mainwindow.show_status_message(
            "Configuration restored")

        self.config_restored.emit()

    def register_config(self, section, default_values):
        if not self._config:
            self._config = {}

        if section not in self._config:
            self._config[section] = default_values

        def getter():
            return self._config[section]
        return getter

    def save_config(self, section, serialised_values):
        self._config[section] = serialised_values
        save_config_file(self._config)

    def start(self):
        self._mainwindow.show()

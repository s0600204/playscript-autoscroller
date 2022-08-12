
from .file_io import (
    load_config_file,
    save_config_file,
)
from .ui.main_window import MainWindow


class Application:

    def __init__(self):
        self._mainwindow = MainWindow(self)

        self._config = None
        self.load_config()

        self._mainwindow.scroll_controller.midpoint_changed.connect(self.save_midpoint)

    def load_config(self):
        self._config = load_config_file()
        if not self._config:
            self._mainwindow.show_status_message(
                "No valid configuration found")
            return

        self._mainwindow.show_status_message(
            "Configuration restored")

        self._mainwindow.scroll_controller.midpoint = self._config['midpoint']

    def save_midpoint(self, new_midpoint):
        self._config['midpoint'] = new_midpoint
        save_config_file(self._config)

    def start(self):
        self._mainwindow.show()

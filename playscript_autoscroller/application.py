
from PyQt5.QtCore import pyqtSignal, QObject

from .file_io import (
    DEFAULT_FILE_TYPE,
    SUPPORTED_FILE_TYPES,
    load_config_file,
    read_document_file,
    save_config_file,
    write_document_file,
)
from .midi_runner import MidiRunner
from .ui.main_window import MainWindow


class Application(QObject):

    config_restored = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._config = None
        self._document_dirty = False
        self._document_filename = None

        self._midi_runner = MidiRunner(self)
        self._mainwindow = MainWindow(self)

        self.load_config()

    @property
    def current_filename(self):
        return self._document_filename

    @property
    def runner(self):
        return self._midi_runner

    @property
    def window(self):
        return self._mainwindow

    def centre_on_screen(self, screen_geometry):
        window_geometry = self._mainwindow.frameGeometry()
        self._mainwindow.move(
            int((screen_geometry.width() - window_geometry.width()) / 2 + screen_geometry.x()),
            int((screen_geometry.height() - window_geometry.height()) / 2 + screen_geometry.y()))

    def file_new(self):
        if self.is_dirty() and not self._mainwindow.prompt_unsaved():
            return

        self._mainwindow.reset_content()
        self._document_filename = None
        self.set_clean()

    def file_open(self):
        self.file_open_with_type(DEFAULT_FILE_TYPE)

    def file_open_with_type(self, filetype):
        if self.is_dirty() and not self._mainwindow.prompt_unsaved():
            return

        filename = self._mainwindow.prompt_open_filename(filetype)
        if not filename:
            return

        filecontent = read_document_file(filename)
        self._mainwindow.restore_content(filetype, filecontent)

        self._document_filename = filename
        self.set_clean()

    def file_save(self):
        return self.file_save_as(self.current_filename)

    def file_save_as(self, filename=None):
        ext = SUPPORTED_FILE_TYPES.get(DEFAULT_FILE_TYPE)[1]
        if not filename or filename[-len(ext):] != ext:
            filename = self._mainwindow.prompt_save_filename()
            if not filename:
                return False

        write_document_file(filename, self._mainwindow.main_text.content)
        self._document_filename = filename
        self.set_clean()
        return True

    def is_dirty(self):
        return self._document_dirty

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

    def set_clean(self):
        self._document_dirty = False
        self._mainwindow.retranslate_title()

    def set_dirty(self):
        self._document_dirty = True
        self._mainwindow.retranslate_title()

    def start(self):
        self._mainwindow.retranslate_ui()
        self._mainwindow.show()

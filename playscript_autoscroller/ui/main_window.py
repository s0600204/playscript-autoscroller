
import os
from os import path

from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from playscript_autoscroller import __app_name__
# ~ from playscript_autoscroller.i18n import translate

from playscript_autoscroller.outline_tree_model import (
    OutlineTreeModel,
    PAGE_FRACTION,
    POSITION_ROLE,
)
from playscript_autoscroller.file_io import (
    DEFAULT_FILE_TYPE,
    SUPPORTED_FILE_TYPES,
)
from .controller import Controller
from .main_text import MainText
from .main_toolbar import MainToolbar
from .menus.about_menu import AboutMenu
from .menus.file_menu import FileMenu
from .outline_tree_view import OutlineTreeView
from .pdf_view import PdfView


class MainWindow(QMainWindow):

    DefaultLocation = path.expanduser('~')
    ConfigKey = 'lastLocation'
    STATUSBAR_MSG_DURATION = 3000 # ms

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.setMinimumSize(640, 480)
        self.resize(1024, 768)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().setContentsMargins(4, 4, 4, 4)
        self._was_maximized = None
        self._content_loading = False

        self._application = application
        self._saved_location = self._application.register_config(
            self.ConfigKey, self.DefaultLocation)
        self._source_view_active = False

        # Menu Bar
        self.menubar = QMenuBar(self)

        self.menu_file = FileMenu(self)
        self.menu_about = AboutMenu(self)

        self.menubar.addMenu(self.menu_file)
        self.menubar.addMenu(self.menu_about)
        self.setMenuBar(self.menubar)

        # Toolbar
        self.toolbar = MainToolbar(self)
        self.addToolBar(self.toolbar)

        self.splitter = QSplitter(parent=self)
        self.splitter.setSizePolicy(
            self.splitter.sizePolicy().horizontalPolicy(),
            QSizePolicy.MinimumExpanding)

        self.outline_model = OutlineTreeModel()
        self.outline_tree = OutlineTreeView(self.outline_model, parent=self.splitter)
        self.splitter.addWidget(self.outline_tree)
        self.splitter.setStretchFactor(0, 1)

        # Content
        self.content_holder = QWidget(parent=self.splitter)
        self.content_holder.setLayout(QVBoxLayout())
        self.content_holder.layout().setContentsMargins(0, 0, 0, 0)

        self.main_text = MainText(application, self.toolbar, parent=self.content_holder)
        self.toolbar.connect_textfield(self.main_text)
        self.main_text.textChanged.connect(self.on_textcontent_change)
        self.content_holder.layout().addWidget(self.main_text)

        self.pdf_view = PdfView(application, parent=self.content_holder)
        self.pdf_view.setVisible(False)
        self.content_holder.layout().addWidget(self.pdf_view)

        self.splitter.addWidget(self.content_holder)
        self.splitter.setStretchFactor(1, 5)
        self.outline_tree.pressed.connect(self.on_outline_press)

        self.centralWidget().layout().addWidget(self.splitter)

        # Controller
        self.scroll_controller = Controller(self._application, parent=self)
        self.centralWidget().layout().addWidget(self.scroll_controller)

        # Scroll Timer
        self.text_scroll_timer = QTimer()
        self.text_scroll_timer.setInterval(100)
        self.text_scroll_timer.timeout.connect(self.slider_scroll_tick)
        self.text_scroll_timer.start()

    @property
    def pdf_view_active(self):
        return self.pdf_view.isVisible()

    @property
    def source_view_active(self):
        return self._source_view_active

    @property
    def toc_active(self):
        return self.outline_model.has_content

    def closeEvent(self, event):
        # pylint: disable=invalid-name
        if self.prompt_unsaved():
            return event.accept()
        return event.ignore()

    def enable_outline(self, enable):
        self.show_outline(enable and self.toolbar.should_show_outline())

    def get_valid_location(self):
        candidate = self._saved_location()
        if not candidate:
            return self.DefaultLocation

        while not path.exists(candidate):
            candidate = path.dirname(candidate)
        if os.access(candidate, os.R_OK | os.W_OK):
            return candidate

        return self.DefaultLocation

    def on_outline_press(self, index):
        idx = self.outline_model.data(index, POSITION_ROLE)
        if self.pdf_view_active:
            self.pdf_view.go_to_page(idx, self.outline_model.data(index, PAGE_FRACTION))
        else:
            self.main_text.go_to_position(idx)

    def on_textcontent_change(self):
        if self.pdf_view_active or self._source_view_active or self._content_loading:
            return
        self.rebuild_outline()

    def open_midi_config(self):
        self._application.runner.open_config_dialog(self)

    def prompt_open_filename(self, filetype='markdown'):
        location = self.get_valid_location()
        filetypedef = SUPPORTED_FILE_TYPES.get(filetype)
        caption = "Select file to open..."
        if filetype != DEFAULT_FILE_TYPE:
            caption = "Select file to import..."

        response = QFileDialog.getOpenFileName(
            self,           # parent
            caption,        # caption
            location,       # directory / dir [pyqt/pyside]
            filetypedef[0]) # filter

        if not response[0]:
            return None

        new_location = path.dirname(response[0])
        if new_location != location:
            self._application.save_config(self.ConfigKey, new_location)

        return response[0]

    def prompt_save_filename(self):
        location = self.get_valid_location()
        filetypedef = SUPPORTED_FILE_TYPES.get(DEFAULT_FILE_TYPE)

        response = QFileDialog.getSaveFileName(
            self,           # parent
            "Save as...",   # caption
            location,       # directory / dir [pyqt5/pyside]
            filetypedef[0]) # filter

        if not response[0]:
            return None

        new_location = path.dirname(response[0])
        if new_location != location:
            self._application.save_config(self.ConfigKey, new_location)

        file_ext = filetypedef[1]
        if response[0][-len(file_ext):] == file_ext:
            return response[0]

        return f"{response[0]}{file_ext}"

    def prompt_unsaved(self):
        if not self._application.is_dirty():
            return True

        # Prompt user if the want to save/saveAs
        question = QMessageBox()
        question.setText("The document has been modified.")
        question.setInformativeText("Do you want to save your changes?")
        question.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        question.setDefaultButton(QMessageBox.Save)
        response = question.exec()

        # If they do,
        if response == QMessageBox.Cancel:
            return False
        if response == QMessageBox.Discard:
            return True

        return self._application.file_save()

    def slider_scroll_tick(self):
        difference, interval = self.scroll_controller.value()
        if self.pdf_view_active:
            self.pdf_view.scroll(difference)
        else:
            self.main_text.scroll(difference)
        self.text_scroll_timer.setInterval(interval)

    def rebuild_outline(self):
        self.outline_model.determine_outline(self.main_text.document())
        self.outline_tree.expandAll()

    def reset_content(self):
        self.main_text.setVisible(True)
        self.pdf_view.setVisible(False)
        self.main_text.clear()
        self.outline_model.clear()
        self.pdf_view.clear()

    def restore_content(self, filetype, filecontent):
        self._content_loading = True
        self.reset_content()
        self.show_source_view(False)
        if filetype == 'markdown':
            self.main_text.setMarkdown(filecontent)
        elif filetype == 'rst':
            self.main_text.setReStructuredText(filecontent)
        self.main_text.respace_text()
        self.toolbar.update_enabled_buttons()
        self.rebuild_outline()
        self._content_loading = False

    def retranslate_title(self):
        filename = self._application.current_filename
        filename = path.basename(filename) if filename else 'Untitled'
        dirty = '*' if self._application.is_dirty() else ''
        self.setWindowTitle(f"{__app_name__} - {filename}{dirty}")

    def retranslate_ui(self):
        self.retranslate_title()

        self.menu_file.retranslate_ui()
        self.menu_about.retranslate_ui()

        self.toolbar.retranslate_ui()

        self.scroll_controller.retranslate_ui()

    def set_fullscreen(self, enable):
        if enable:
            self._was_maximized = self.windowState() & Qt.WindowMaximized
            self.showFullScreen()
        elif self._was_maximized:
            self.showMaximized()
        else:
            self.showNormal()

    def show_outline(self, show):
        if show:
            self.outline_tree.show()
        else:
            self.outline_tree.hide()

    def show_pdf(self, pdf_document):
        self.reset_content()
        self.main_text.setVisible(False)
        self.pdf_view.set_pdf(pdf_document)
        self.pdf_view.setVisible(True)
        self.outline_model.determine_from_pdf(pdf_document)
        self.outline_tree.expandAll()
        self.toolbar.update_enabled_buttons() # Must be after pdf_view.setVisible()

    def show_source_view(self, show):
        if self.pdf_view_active:
            return
        self._source_view_active = show
        self.main_text.show_source_view(show)
        self.toolbar.update_source_view_checked()
        self.toolbar.update_enabled_buttons()

        if not show:
            self.rebuild_outline()

    def show_status_message(self, message):
        self.statusBar().showMessage(
            message,
            self.STATUSBAR_MSG_DURATION
        )

    def zoom_in(self, _):
        if self.pdf_view_active:
            self.pdf_view.zoom_in()
        else:
            self.main_text.zoom_in()

    def zoom_out(self, _):
        if self.pdf_view_active:
            self.pdf_view.zoom_out()
        else:
            self.main_text.zoom_out()

    def zoom_reset(self, _):
        if self.pdf_view_active:
            self.pdf_view.zoom_reset()
        else:
            self.main_text.zoom_reset()

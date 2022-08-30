
from os import path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from script_scroller import __app_name__
# ~ from script_scroller.i18n import translate

from script_scroller.outline_tree_model import OutlineTreeModel, POSITION_ROLE
from .controller import Controller
from .main_text import MainText
from .main_toolbar import MainToolbar
# ~ from .menus.about_menu import AboutMenu
# ~ from .menus.edit_menu import EditMenu
from .menus.file_menu import FileMenu
from .outline_tree_view import OutlineTreeView


class MainWindow(QMainWindow):

    STATUSBAR_MSG_DURATION = 3000 # ms

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.setMinimumSize(640, 480)
        self.resize(1024, 768)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().setContentsMargins(4, 4, 4, 4)
        self._was_maximized = None

        self._application = application

        # Menu Bar
        self.menubar = QMenuBar(self)

        self.menu_file = FileMenu(self)
        # ~ self.menu_edit = EditMenu(self)
        # ~ self.menu_about = AboutMenu(self)

        self.menubar.addMenu(self.menu_file)
        # ~ self.menubar.addMenu(self.menu_edit)
        # ~ self.menubar.addMenu(self.menu_about)
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
        self.main_text = MainText(application, self.toolbar, parent=self.splitter)
        self.splitter.addWidget(self.main_text)
        self.splitter.setStretchFactor(1, 5)
        self.toolbar.connect_textfield(self.main_text)
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

    def closeEvent(self, event):
        # pylint: disable=invalid-name
        if self.prompt_unsaved():
            return event.accept()
        return event.ignore()

    def on_outline_press(self, index):
        self.main_text.go_to_position(
            self.outline_model.data(index, POSITION_ROLE))

    def open_midi_config(self):
        self._application.runner.open_config_dialog(self)

    def prompt_open_filename(self):
        # parent = nullptr,
        # caption = QString(),
        # directory = QString(),
        # filter = QString(),
        # selectedFilter = nullptr,
        # options = Options()
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select file to open...",
            directory="~/",
            filter="Scripts (*.md)")

        return response[0] or None

    def prompt_save_filename(self):
        # parent = nullptr,
        # caption = QString()
        # directory = QString()
        # filter = QString()
        # selectedFilter = nullptr
        # options = Options()
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save as...",
            directory="~/",
            filter="Scripts (*.md)")

        if not response[0]:
            return None

        if response[0][-3:] == '.md':
            return response[0]

        return response[0] + '.md'

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
        self.main_text.scroll(self.scroll_controller.value())

    def rebuild_outline(self):
        self.outline_model.determine_outline(self.main_text.document())
        self.outline_tree.expandAll()

    def reset_content(self):
        self.main_text.clear()
        self.outline_model.clear()

    def restore_content(self, filecontent):
        self.reset_content()
        self.show_source_view(False)
        self.main_text.setMarkdown(filecontent)
        self.main_text.respace_text()
        self.rebuild_outline()

    def retranslate_title(self):
        filename = self._application.current_filename
        filename = path.basename(filename) if filename else 'Untitled'
        dirty = '*' if self._application.is_dirty() else ''
        self.setWindowTitle(f"{__app_name__} - {filename}{dirty}")

    def retranslate_ui(self):
        self.retranslate_title()

        # Menus
        self.menu_file.retranslate_ui()
        # ~ self.menu_edit.retranslate_ui()
        # ~ self.menu_about.retranslate_ui()

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

    def show_source_view(self, show):
        self.main_text.show_source_view(show)
        self.toolbar.set_source_view_checked(show)
        self.toolbar.set_text_formatting_enabled(not show)

        if show:
            self.outline_tree.hide()
        else:
            self.rebuild_outline()
            if self.toolbar.should_show_outline():
                self.outline_tree.show()

    def show_status_message(self, message):
        self.statusBar().showMessage(
            message,
            self.STATUSBAR_MSG_DURATION
        )

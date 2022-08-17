
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QSizePolicy,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget,

    QSlider,
    QTextEdit,
)

from script_scroller import __app_name__
# ~ from script_scroller.i18n import translate

from script_scroller.outline_tree_model import OutlineTreeModel
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
        self.splitter.setStretchFactor(1, 2)
        self.toolbar.connect_textfield(self.main_text)

        self.centralWidget().layout().addWidget(self.splitter)

        self.scroll_controller = Controller(self._application, parent=self)
        self.centralWidget().layout().addWidget(self.scroll_controller)

        self.text_scroll_timer = QTimer()
        self.text_scroll_timer.setInterval(100)
        self.text_scroll_timer.timeout.connect(self.slider_scroll_tick)
        self.text_scroll_timer.start()

    def open_midi_config(self):
        self._application.runner.open_config_dialog(self)

    def slider_scroll_tick(self):
        self.main_text.scroll(self.scroll_controller.value())

    def retranslate_ui(self):
        self.setWindowTitle(__app_name__)

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

    def show_source_view(self, show):
        self.main_text.show_source_view(show)
        self.toolbar.set_text_formatting_enabled(not show)

        if show:
            self.outline_tree.hide()
        else:
            self.outline_model.determine_outline(self.main_text.document())
            self.outline_tree.expandAll()
            self.outline_tree.show()

    def show_status_message(self, message):
        self.statusBar().showMessage(
            message,
            self.STATUSBAR_MSG_DURATION
        )

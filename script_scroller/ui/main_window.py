
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,

    QVBoxLayout,
    QWidget,

    QSlider,
    QTextEdit,
)

from script_scroller import __app_name__
# ~ from script_scroller.i18n import translate

from .controller import Controller
# ~ from .menus.about_menu import AboutMenu
# ~ from .menus.edit_menu import EditMenu
from .menus.file_menu import FileMenu


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


        # Content
        self.text_slider = QSlider(Qt.Horizontal, self)
        self.text_slider.setTickPosition(QSlider.TicksBelow)
        self.text_slider.setMinimum(0)
        self.text_slider.setMaximum(127)
        self.text_slider.valueChanged.connect(self.slider_change)
        self.centralWidget().layout().addWidget(self.text_slider)

        self.text_holder = QTextEdit(self)
        _text = ""
        for i in range(128):
            _text += str(i) + "\n"
        self.text_holder.setText(_text)
        self.centralWidget().layout().addWidget(self.text_holder)

        self.scroll_controller = Controller(self)
        self.centralWidget().layout().addWidget(self.scroll_controller)

        self.text_scroll_timer = QTimer()
        self.text_scroll_timer.setInterval(100)
        self.text_scroll_timer.timeout.connect(self.slider_scroll_tick)
        self.text_scroll_timer.start()

        self.retranslate_ui()
        self.load_config()

    def load_config(self):
        # @todo: Actually save and load a config
        self.scroll_controller.midpoint = 63
        self.text_slider.setValue(60)

    def slider_change(self, *_):
        self.scroll_controller.update(self.text_slider.value())

    def slider_scroll_tick(self):
        scrollbar = self.text_holder.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + self.scroll_controller.value())

    def retranslate_ui(self):
        self.setWindowTitle(__app_name__)

        # Menus
        self.menu_file.retranslate_ui()
        # ~ self.menu_edit.retranslate_ui()
        # ~ self.menu_about.retranslate_ui()

        self.scroll_controller.retranslate_ui()

    def set_fullscreen(self, enable):
        if enable:
            self._was_maximized = self.windowState() & Qt.WindowMaximized
            self.showFullScreen()
        elif self._was_maximized:
            self.showMaximized()
        else:
            self.showNormal()

    def show_status_message(self, message):
        self.statusBar().showMessage(
            message,
            self.STATUSBAR_MSG_DURATION
        )

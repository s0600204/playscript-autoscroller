
import sys

from qtpy.QtCore import QTimer
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication

import qdarktheme

from . import __app_icon__, __app_name__
from .application import Application

def main():
    # Create the QApplication
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName(__app_name__)
    qt_app.setQuitOnLastWindowClosed(True)

    custom = {
        "border": "#5a5a62",
        "foreground": "#d4d4e4",
        "background": "#1a1a1a",
        "primary": "#9f8af7",
    }
    qt_app.setPalette(qdarktheme.load_palette(custom_colors=custom))
    qt_app.setStyleSheet(qdarktheme.load_stylesheet(custom_colors=custom))

    qt_app.setWindowIcon(QIcon(__app_icon__))

    # Initialize the application
    app = Application()
    app.centre_on_screen(qt_app.primaryScreen().geometry())

    # Run the application
    QTimer.singleShot(0, app.start)
    exit_code = qt_app.exec()

    # Cleanup
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


#from os import path
import sys

from PyQt5.QtCore import QTimer
#from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import qdarkstyle

from . import __app_name__
from .application import Application

def main():
    # Create the QApplication
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName(__app_name__)
    qt_app.setQuitOnLastWindowClosed(True)

    qt_app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    # ~ qt_app.setWindowIcon(
        # ~ QIcon(f"{path.dirname(__file__)}/ui/icons/mic_rx_monitor.svg")
    # ~ )

    # Initialize the application
    app = Application()

    # Run the application
    QTimer.singleShot(0, app.start)
    exit_code = qt_app.exec()

    # Cleanup
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

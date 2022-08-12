
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QProgressBar,
    QPushButton,
    QSlider,
    QWidget,
)


class Controller(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self._status = QProgressBar(self)
        self._status.setRange(0, 127)
        self._status.setTextVisible(False)
        self.layout().addWidget(self._status, 0, 0)

        self._midpoint = QSlider(Qt.Horizontal, self)
        self._midpoint.setMinimum(0)
        self._midpoint.setMaximum(127)
        self._midpoint.setTickPosition(QSlider.TicksAbove)
        self.layout().addWidget(self._midpoint, 1, 0)

        self._ignore_button = QPushButton(self)
        self._ignore_button.setCheckable(True)
        self._ignore_button.setChecked(True)
        self.layout().addWidget(self._ignore_button, 0, 1, 2, 1)

    @property
    def midpoint(self):
        """Value that is the midpoint of the input."""
        return self._midpoint.value()

    @midpoint.setter
    def midpoint(self, new_midpoint):
        self._midpoint.setValue(new_midpoint)
        self._status.setValue(new_midpoint)

    def retranslate_ui(self):
        self._ignore_button.setText('Ignore')

    def update(self, new_value):
        self._status.setValue(new_value)

    def value(self):
        if self._ignore_button.isChecked():
            return 0

        # @todo: Implement a better way of translating values to something that can used to scroll
        return round((self._status.value() - self._midpoint.value()) / 4)

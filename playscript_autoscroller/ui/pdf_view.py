
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from popplerqt5 import Poppler


class PdfView(QScrollArea):

    DefaultZoom = 100
    ZoomConfigKey = 'zoom_pdf'

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._application = application

        self.setAlignment(Qt.AlignHCenter)
        self.setWidgetResizable(True)

        self.main_container = QWidget()
        self.main_container.setLayout(QVBoxLayout())
        self.main_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWidget(self.main_container)

        self.page_images = []
        self._pdf = None
        self._zoom_percentage = self._application.register_config(self.ZoomConfigKey, self.DefaultZoom)

    def clear(self):
        # @todo: scroll to top of area, (?conditionally - don't want to do that on zoom)
        layout = self.main_container.layout()
        while not layout.isEmpty():
            layout_item = layout.takeAt(0)
            layout_item.widget().deleteLater()

    def render(self):
        if not self._pdf:
            return

        screen = self._application.window.screen()
        dpi = screen.physicalDotsPerInch()
        if not dpi:
            dpi = screen.logicalDotsPerInch()
        percentage = self._zoom_percentage() / 100
        zoom_dpi = dpi * percentage

        for page in self._pdf:
            rendered = page.renderToImage(zoom_dpi, zoom_dpi)

            page_image = QLabel()
            page_image.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            page_image.setPixmap(QPixmap.fromImage(rendered))
            self.main_container.layout().addWidget(page_image)

    def scroll(self, step):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + step)

    def set_pdf(self, pdf_document):
        pdf_document.setRenderHint(Poppler.Document.RenderHint.Antialiasing, True)
        pdf_document.setRenderHint(Poppler.Document.RenderHint.TextAntialiasing, True)
        self._pdf = pdf_document
        self.render()

    def zoom_in(self):
        percentage = self._zoom_percentage()
        if percentage >= 300:
            return
        self._application.save_config(self.ZoomConfigKey, percentage + 10)
        self.clear()
        self.render()

    def zoom_out(self):
        percentage = self._zoom_percentage()
        if percentage <= 10:
            return
        self._application.save_config(self.ZoomConfigKey, percentage - 10)
        self.clear()
        self.render()

    def zoom_reset(self):
        self._application.save_config(self.ZoomConfigKey, self.DefaultZoom)
        self.clear()
        self.render()

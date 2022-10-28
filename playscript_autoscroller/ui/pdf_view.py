
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

    ZoomLevel = 96

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(Qt.AlignHCenter)
        self.setWidgetResizable(True)

        self.main_container = QWidget()
        self.main_container.setLayout(QVBoxLayout())
        self.main_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWidget(self.main_container)

        self.page_images = []

        self._pdf = None

    def clear(self):
        # @todo: scroll to top of area
        layout = self.main_container.layout()
        while not layout.isEmpty():
            layout_item = layout.takeAt(0)
            layout_item.widget().deleteLater()

    def render(self):
        if not self._pdf:
            return

        for page in self._pdf:
            rendered = page.renderToImage(self.ZoomLevel, self.ZoomLevel)

            page_image = QLabel()
            page_image.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            page_image.setPixmap(QPixmap.fromImage(rendered))
            self.main_container.layout().addWidget(page_image)

    def set_pdf(self, pdf_document):
        pdf_document.setRenderHint(Poppler.Document.RenderHint.Antialiasing, True)
        pdf_document.setRenderHint(Poppler.Document.RenderHint.TextAntialiasing, True)
        self._pdf = pdf_document
        self.render()

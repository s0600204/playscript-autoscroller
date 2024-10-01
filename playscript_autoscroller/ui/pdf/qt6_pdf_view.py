
from qtpy.QtCore import QPointF
from qtpy.QtPdf import QPdfDocument
from qtpy.QtPdfWidgets import QPdfView


class Qt6PdfView(QPdfView):

    DefaultZoom = 100
    ZoomConfigKey = 'zoom_pdf'

    def __init__(self, application, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._application = application

        self.setPageMode(QPdfView.PageMode.MultiPage)
        self.setZoomMode(QPdfView.ZoomMode.Custom)

        self._zoom_percentage = \
            self._application.register_config(self.ZoomConfigKey, self.DefaultZoom)

    def clear(self):
        self.setDocument(QPdfDocument(self))

    def go_to_page(self, page_index, page_fraction=0):
        navigator = self.pageNavigator()
        navigator.jump(page_index, page_fraction)

    def scroll(self, step):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + step)

    def set_pdf(self, pdf_document):
        self.setDocument(pdf_document)

    def zoom_in(self):
        percentage = self._zoom_percentage()
        if percentage >= 300:
            return
        percentage += 10
        self._application.save_config(self.ZoomConfigKey, percentage)
        self.setZoomFactor(percentage / 100)

    def zoom_out(self):
        percentage = self._zoom_percentage()
        if percentage <= 10:
            return
        percentage -= 10
        self._application.save_config(self.ZoomConfigKey, percentage)
        self.setZoomFactor(percentage / 100)

    def zoom_reset(self):
        self._application.save_config(self.ZoomConfigKey, self.DefaultZoom)
        self.setZoomFactor(self.DefaultZoom / 100)

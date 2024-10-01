
from ..pdf import PDF_SUPPORT, PdfLibrary

if PDF_SUPPORT is PdfLibrary.Poppler:
    from .pdf.poppler_pdf_view import PopplerPdfView as PdfView

elif PDF_SUPPORT is PdfLibrary.QtPdf:
    from .pdf.qt6_pdf_view import Qt6PdfView as PdfView

else:
    from .pdf.dummy_pdf_view import DummyPdfView as PdfView

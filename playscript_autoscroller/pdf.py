# pylint: disable=ungrouped-imports

from enum import auto, Enum

import qtpy

class PdfLibrary(Enum):
    # pylint: disable=invalid-name
    Disabled=auto()
    Poppler=auto()
    QtPdf=auto()

PDF_SUPPORT = PdfLibrary.Disabled

if qtpy.PYQT5:
    try:
        # pylint: disable=unused-import
        import popplerqt5
        PDF_SUPPORT = PdfLibrary.Poppler
    except ModuleNotFoundError:
        pass

elif qtpy.QT6:
    try:
        import qtpy.QtPdf
        PDF_SUPPORT = PdfLibrary.QtPdf
    except ImportError:
        pass

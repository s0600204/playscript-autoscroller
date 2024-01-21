
from enum import auto, Enum

import qtpy

class PdfLibrary(Enum):
    Disabled=auto()
    Poppler=auto()

PDF_SUPPORT = PdfLibrary.Disabled

if qtpy.PYQT5:
    try:
        import popplerqt5
        PDF_SUPPORT = PdfLibrary.Poppler
    except ModuleNotFoundError:
        pass


from datetime import datetime
from os import makedirs, path, rename

from strictyaml import (
    as_document,
    load as yaml_load,
    YAMLValidationError,
)

from .pdf import PDF_SUPPORT, PdfLibrary
if PDF_SUPPORT is PdfLibrary.Poppler:
    from popplerqt5 import Poppler
if PDF_SUPPORT is PdfLibrary.QtPdf:
    from qtpy.QtPdf import QPdfDocument

from . import __config_file__
from .schema import config_schema


DEFAULT_FILE_TYPE = 'rst'
SUPPORTED_FILE_TYPES = {
    'markdown': ('Playscripts (*.md)', '.md'),
    'pdf': ('PDF Documents (*.pdf)', '.pdf'),
    'rst': ('Playscripts (*.rst)', '.rst'),
}

def load_pdf_file(filename, application):
    if PDF_SUPPORT is PdfLibrary.Poppler:
        return Poppler.Document.load(filename)

    if PDF_SUPPORT is PdfLibrary.QtPdf:
        pdf_document = QPdfDocument(application)
        pdf_document.load(filename)
        return pdf_document

    return None

def load_yaml_file(filepath, schema):
    """Note: this function does not perform any handling of Errors or Exceptions."""
    with open(filepath, mode='r', encoding='utf-8') as filehandle:
        return yaml_load(
            filehandle.read(),
            schema,
            label=path.basename(filepath)
        ).data

def read_document_file(filepath):
    with open(filepath, mode='r', encoding='utf-8') as filehandle:
        return filehandle.read()

def write_document_file(filepath, content):
    with open(filepath, mode='w', encoding='utf-8') as filehandle:
        return filehandle.write(
            content
        )

def write_yaml_file(filepath, schema, content):
    yaml = as_document(content, schema)
    with open(filepath, mode='w', encoding='utf-8') as filehandle:
        return filehandle.write(
            yaml.as_yaml()
        )

def load_config_file():
    if path.exists(__config_file__):
        try:
            return load_yaml_file(__config_file__, config_schema)
        except YAMLValidationError:
            # Invalid config file. Rename it so it's saved, but out the way.
            _dire = path.dirname(__config_file__)
            _name = path.basename(__config_file__)
            _time = datetime.utcnow().isoformat(timespec='seconds')
            rename(__config_file__, path.join(_dire, f"{_time}_{_name}.rej"))
    return {}

def save_config_file(config):
    if not path.exists(__config_file__):
        makedirs(path.dirname(__config_file__), exist_ok=True)

    config['lastSave'] = datetime.utcnow()
    return write_yaml_file(__config_file__, config_schema, config)

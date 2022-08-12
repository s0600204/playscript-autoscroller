
from datetime import datetime
from os import makedirs, path, rename

from strictyaml import (
    as_document,
    load as yaml_load,
    YAMLValidationError,
)

from . import __config_file__
from .schema import config_schema


def load_yaml_file(filepath, schema):
    """Note: this function does not perform any handling of Errors or Exceptions."""
    with open(filepath, mode='r', encoding='utf-8') as filehandle:
        return yaml_load(
            filehandle.read(),
            schema,
            label=path.basename(filepath)
        ).data

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

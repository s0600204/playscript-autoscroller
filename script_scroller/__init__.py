
from os import path

from appdirs import AppDirs


_app_dirs = AppDirs(
    "ScriptScroller"
)


__app_name__ = "Script Scroller"
__doc__ = "MIDI-controllable Playscript Scroller"
__config_file__ = path.join(_app_dirs.user_config_dir, "config.yaml")

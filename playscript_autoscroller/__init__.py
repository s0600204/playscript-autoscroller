
from importlib.metadata import PackageNotFoundError, version
from os import path

from appdirs import AppDirs


_app_dirs = AppDirs(
    "PlayscriptAutoscroller"
)

# Not SemVer! (unfortunately)
def _split_vers(vers):
    vers = vers.split(".")

    # Major.Minor.*
    #   0.1.*
    #   1.0.*
    for idx in range(2):
        vers[idx] = int(vers[idx])

    # *.Patch[prerelease].*
    #   *.1
    #   *.1.*
    #   *.1a0
    #   *.1c2.*
    patch_vers = vers[2]
    if patch_vers.isnumeric():
        vers[2] = int(patch_vers)
    else:
        for char in patch_vers:
            if char.isnumeric():
                continue
            idx = patch_vers.index(char)
            vers[2:3] = int(patch_vers[0:idx]), patch_vers[idx:]
            break

    # *.?
    #   *.dev0+gAbCdEfGh
    #   *.d20220104
    #   *.dev14+gAbCdEfGh.d20220104
    for idx in range(3, len(vers)):
        vers[idx:idx+1] = vers[idx].split("+")

    return tuple(vers)


__app_name__ = "Playscript Autoscroller"
__app_icon__ = f"{path.dirname(__file__)}/ui/icons/playscript-autoscroller.svg"
__author__ = "s0600204"
__doc__ = "MIDI-controllable autoscroller for theatre playscripts"
__config_file__ = path.join(_app_dirs.user_config_dir, "config.yaml")
__version__ = version(path.split(path.dirname(__file__))[-1])
__version_info__ = _split_vers(__version__)

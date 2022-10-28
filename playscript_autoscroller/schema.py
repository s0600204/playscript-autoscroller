
from strictyaml import (
    Datetime,
    Int,
    Map,
    Str,
)

"""
lastSave: [[ISO-8601 DateTime]]
lastLocation: "/home/user"
midpoint: 63
midi:
  device: "DeviceName:PortName DeviceNum:PortNum"
  channel: 1
  control: 7
zoom_pdf: 100
zoom_text: 2
"""

config_schema = Map({
    "lastSave": Datetime(),
    "lastLocation": Str(),
    "midpoint": Int(),
    "midi": Map({
      "device": Str(),
      "channel": Int(),
      "scroll_control": Int(),
      "midpoint_control": Int(),
      "ignore_note": Int(),
      "pause_note": Int(),
    }),
    "zoom_pdf": Int(),
    "zoom_text": Int(),
})

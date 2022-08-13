
from strictyaml import (
    Datetime,
    Int,
    Map,
    Str,
)

"""
lastSave: [[ISO-8601 DateTime]],
midpoint: 63
midi:
  device: "DeviceName:PortName DeviceNum:PortNum"
  channel: 1
  control: 7
"""

config_schema = Map({
    "lastSave": Datetime(),
    "midpoint": Int(),
    "midi": Map({
      "device": Str(),
      "channel": Int(),
      "control": Int(),
    }),
})

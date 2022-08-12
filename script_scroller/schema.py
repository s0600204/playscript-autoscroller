
from strictyaml import (
    Datetime,
    Int,
    Map,
)

"""
lastSave: [[ISO-8601 DateTime]],
midpoint: 63
"""

config_schema = Map({
    "lastSave": Datetime(),
    "midpoint": Int(),
})

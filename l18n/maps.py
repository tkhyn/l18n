from .translation import TransDict

try:
    from . import __maps
    tz_locations = TransDict(__maps.tz_locations)
    territories = TransDict(__maps.territories)
except ImportError:
    tz_locations = {}
    territories = {}

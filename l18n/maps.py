from .translation import L18NDict

try:
    from . import __maps
    tz_locations = L18NDict(__maps.tz_locations)
    territories = L18NDict(__maps.territories)
except ImportError:
    tz_locations = {}
    territories = {}

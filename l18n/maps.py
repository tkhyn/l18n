from .translation import L18NDict

try:
    from . import __maps
    tz_cities = L18NDict(__maps.tz_cities)
    territories = L18NDict(__maps.territories)
except ImportError:
    tz_cities = {}
    territories = {}

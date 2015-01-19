from .translation import L18NDict, L18NListDict

try:
    from . import __maps
    tz_cities = L18NDict(__maps.tz_cities)
    tz_fullnames = L18NListDict('/', __maps.tz_cities, **__maps.tz_locations)
    territories = L18NDict(__maps.territories)
except ImportError:
    tz_cities = {}
    tz_fullnames = {}
    territories = {}

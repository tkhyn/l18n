from .translation import L18NMap, L18NListMap

try:
    from . import __maps
    tz_cities = L18NMap(__maps.tz_cities)
    tz_fullnames = L18NListMap('/', __maps.tz_cities, **__maps.tz_locations)
    territories = L18NMap(__maps.territories)
except ImportError:
    tz_cities = {}
    tz_fullnames = {}
    territories = {}

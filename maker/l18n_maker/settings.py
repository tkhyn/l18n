import os

LOCALES = ('en', 'fr')

CLDR_TZ_CITIES_URL = \
'http://www.unicode.org/repos/cldr-aux/charts/26/by_type/timezones.timezone_cities.html'
CLDR_TERRITORIES_URL = \
'http://www.unicode.org/repos/cldr-aux/charts/26/by_type/locale_display_names.territories.html'

LOCALE_PATH = os.path.join(
    os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2]),
    'l18n', 'locale'
)

PO_PATH = os.path.join(LOCALE_PATH, '%s', 'LC_MESSAGES', 'l18n.po')

PY_PATH = os.path.join(
    os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2]),
    'l18n', '__maps.py'
)

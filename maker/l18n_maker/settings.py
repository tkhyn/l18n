import os

# IMPORTANT: 'en' is the default locale and should not be included in LOCALES
LOCALES = ('fr',)

CLDR_DATA_URL = 'http://www.unicode.org/Public/cldr/latest'

LOCALE_PATH = os.path.join(
    os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2]),
    'l18n', 'locale'
)

PO_PATH = os.path.join(LOCALE_PATH, '%s', 'LC_MESSAGES', 'l18n.po')

PY_PATH = os.path.join(
    os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2]),
    'l18n', '__maps.py'
)

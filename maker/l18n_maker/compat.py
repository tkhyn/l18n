try:
    # python 3
    import configparser
    configparser.ConfigParser.optionxform = str
except ImportError:
    # python 2
    import ConfigParser as configparser
    configparser.ConfigParser.optionxform = unicode

try:
    # python 2
    import urllib.request as urllib2
except ImportError:
    # python 3
    import urllib2

try:
    # python 2
    from __builtin__ import unicode
except ImportError:
    # python 3
    unicode = str

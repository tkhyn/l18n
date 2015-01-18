try:
    # python 3
    import configparser
    configparser.ConfigParser.optionxform = str
except ImportError:
    # python 2
    import ConfigParser as configparser
    configparser.ConfigParser.optionxform = unicode

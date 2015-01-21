try:
    # python 2
    from __builtin__ import unicode
except ImportError:
    # python 3
    unicode = str

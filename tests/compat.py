try:
    # python 3
    from importlib import reload
except ImportError:
    # python 2
    from imp import reload

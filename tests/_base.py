try:
    import unittest2 as unittest
except ImportError:
    import unittest

# nose should not look for tests in this module
__test__ = False
__unittest = True


class TestCase(unittest.TestCase):
    pass

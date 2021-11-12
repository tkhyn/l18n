import unittest

import l18n

# nose should not look for tests in this module
__test__ = False
__unittest = True


class TestCase(unittest.TestCase):

    language = None

    @classmethod
    def setUpClass(cls):
        l18n.set_language(cls.language)

    @classmethod
    def tearDownClass(cls):
        l18n.set_language(None)

import l18n

from ._base import TestCase


class TranslationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        l18n.set_language('fr')

    @classmethod
    def tearDownClass(cls):
        l18n.set_language(None)

    def test_tz_city_translated(self):
        self.assertEqual(str(l18n.tz_cities['Canada/Newfoundland']),
                         u'Terre-Neuve')

    def test_territory_translated(self):
        self.assertEqual(str(l18n.territories['ES']), u'Espagne')

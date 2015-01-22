import l18n

from ._base import TestCase
from ._compat import unicode


class DictBehaviorTests(TestCase):

    def test_get(self):
        for k in l18n.tz_cities:
            self.assertEqual(
                unicode(l18n.tz_fullnames.get(k)),
                unicode(l18n.tz_fullnames[k])
            )

    def test_items(self):
        items = l18n.tz_fullnames.items()
        for i, v in items:
            self.assertEqual(unicode(v), unicode(l18n.tz_fullnames[i]))

    def test_locations_and_cities_keys(self):
        self.assertEqual(set(l18n.tz_cities.keys()),
                         set(l18n.tz_fullnames.keys()))

    def test_delete_UTC(self):
        # UTC is not a timezone properly speaking, let's remove it
        utc = l18n.tz_cities['UTC']
        del l18n.tz_cities['UTC']
        with self.assertRaises(KeyError):
            unicode(l18n.tz_cities['UTC'])
        l18n.tz_cities['UTC'] = utc

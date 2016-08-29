import l18n
import six

from ._base import TestCase


class DictBehaviorTests(TestCase):

    def test_get(self):
        for k in l18n.tz_cities:
            self.assertEqual(
                six.text_type(l18n.tz_fullnames.get(k)),
                six.text_type(l18n.tz_fullnames[k])
            )

    def test_items(self):
        items = l18n.tz_fullnames.items()
        for i, v in items:
            self.assertEqual(six.text_type(v), six.text_type(l18n.tz_fullnames[i]))

    def test_locations_and_cities_keys(self):
        self.assertEqual(set(l18n.tz_cities.keys()),
                         set(l18n.tz_fullnames.keys()))

    def test_delete_UTC(self):
        # UTC is not a timezone properly speaking, let's remove it
        del l18n.tz_cities['UTC']
        with self.assertRaises(KeyError):
            six.text_type(l18n.tz_cities['UTC'])
        # re-add it afterwards
        l18n.tz_cities['UTC'] = 'UTC'

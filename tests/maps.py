import l18n
import six
import pytz

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

    def test_repr(self):
        # test that all lazy strings are `repr`-ed correctly
        [repr(tz) for tz in l18n.tz_fullnames.values()]


class SortingTests(TestCase):

    language = 'en'

    def test_tz_fullnames_sorting(self):
        keys = list(l18n.tz_fullnames)
        self.assertEqual(keys[0], 'Africa/Abidjan')
        self.assertEqual(keys[-1], 'Zulu')

    def test_tz_cities_sorting(self):
        keys = list(l18n.tz_cities)
        self.assertEqual(keys[0], 'Australia/ACT')
        self.assertEqual(keys[-1], 'Europe/Zurich')


class SubsetTests(TestCase):

    def test_subset_tz_fullnames(self):
        nz_tzs = pytz.country_timezones['nz']
        common_tz_fullnames = l18n.tz_fullnames.subset(nz_tzs)
        self.assertListEqual(list(common_tz_fullnames),
                             ['Pacific/Auckland', 'Pacific/Chatham'])

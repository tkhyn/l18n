# -*- coding: utf-8 -*-

import l18n

from ._base import TestCase


class SortingTests(TestCase):

    language = 'en'

    def test_tz_fullname_sorting(self):
        keys = list(l18n.tz_fullnames)
        self.assertEqual(keys[0], 'Africa/Abidjan')
        self.assertEqual(keys[-1], 'Zulu')

    def test_tz_cities_sorting(self):
        keys = list(l18n.tz_cities)
        self.assertEqual(keys[0], 'Australia/ACT')
        self.assertEqual(keys[-1], 'Europe/Zurich')

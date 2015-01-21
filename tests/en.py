# -*- coding: utf-8 -*-

import l18n

from ._base import TestCase


class EnTests(TestCase):

    language = 'en'

    def test_tz_city_translated(self):
        self.assertEqual(str(l18n.tz_cities['Canada/Newfoundland']),
                         u'Newfoundland')

    def test_tz_fullname_translated(self):
        self.assertEqual(
            str(l18n.tz_fullnames['Canada/Newfoundland']),
            u'Canada/Newfoundland'
        )

    def test_territory_translated(self):
        self.assertEqual(str(l18n.territories['ES']), u'Spain')

# -*- coding: utf-8 -*-

import l18n

from ._base import TestCase


class EnTests(TestCase):

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



class FrTests(TestCase):

    @classmethod
    def setUpClass(cls):
        l18n.set_language('fr')

    @classmethod
    def tearDownClass(cls):
        l18n.set_language(None)

    def test_tz_city_translated(self):
        self.assertEqual(str(l18n.tz_cities['Canada/Newfoundland']),
                         u'Terre-Neuve')

    def test_tz_fullname_translated(self):
        self.assertEqual(
            str(l18n.tz_fullnames['America/North_Dakota/New_Salem']),
            u'Amérique/Dakota du Nord/New Salem'
        )

    def test_territory_translated(self):
        self.assertEqual(str(l18n.territories['ES']), u'Espagne')


class DictBehaviorTests(TestCase):

    def test_get(self):
        for k in l18n.tz_cities:
            self.assertEqual(
                str(l18n.tz_fullnames.get(k)), str(l18n.tz_fullnames[k])
            )

    def test_items(self):
        items = l18n.tz_fullnames.items()
        for i, v in items:
            self.assertEqual(str(v), str(l18n.tz_fullnames[i]))

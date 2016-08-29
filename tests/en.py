# -*- coding: utf-8 -*-

import l18n
import six

from ._base import TestCase


class RootTests(TestCase):

    language = None

    def test_tz_city_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_cities['America/North_Dakota/New_Salem']),
            u'New Salem, North Dakota'
        )

    def test_tz_city_override(self):
        self.assertEqual(six.text_type(l18n.tz_cities['Pacific/Easter']),
                         u'Easter Island')

    def test_tz_fullname_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_fullnames['America/North_Dakota/New_Salem']),
            u'America/North Dakota/New Salem'
        )

    def test_territory_translated(self):
        self.assertEqual(six.text_type(l18n.territories['ES']), u'Spain')


class EnTests(TestCase):

    language = 'en'

    def test_tz_city_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_cities['America/North_Dakota/New_Salem']),
            u'New Salem, North Dakota'
        )

    def test_tz_fullname_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_fullnames['America/North_Dakota/New_Salem']),
            u'America/North Dakota/New Salem'
        )

    def test_territory_translated(self):
        self.assertEqual(six.text_type(l18n.territories['ES']), u'Spain')

# -*- coding: utf-8 -*-

import l18n
import six

from .base import TestCase


class FrTests(TestCase):

    language = 'fr'

    def test_tz_city_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_cities['America/North_Dakota/New_Salem']),
            u'New Salem (Dakota du Nord)'
        )

    def test_tz_fullname_translated(self):
        self.assertEqual(
            six.text_type(l18n.tz_fullnames['America/North_Dakota/New_Salem']),
            u'Amérique/Dakota du Nord/New Salem'
        )

    def test_territory_translated(self):
        self.assertEqual(six.text_type(l18n.territories['ES']), u'Espagne')

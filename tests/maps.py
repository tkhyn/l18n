import l18n

from ._base import TestCase


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

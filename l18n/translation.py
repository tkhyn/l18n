import os
import gettext
from locale import getdefaultlocale

import six


class TransDict(dict):

    trans = None

    def __init__(self, *args, **kwargs):
        super(TransDict, self).__init__(*args, **kwargs)
        self.set_language()

    def __getitem__(self, key):
        return self.translate(super(TransDict, self).__getitem__(key))

    if six.PY2:
        def translate(self, s):
            return self.trans.ugettext(s)
    else:
        def translate(self, s):
            return self.trans.gettext(s)

    @classmethod
    def set_language(cls, language=None):
        cls.trans = gettext.translation(
            'l18n',
            os.path.join(os.path.dirname(__file__), 'locale'),
            languages=[language or getdefaultlocale()[0]],
            fallback=True
        )


def set_language(language):
    TransDict.set_language(language)

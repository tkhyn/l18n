import os
import gettext
from locale import getdefaultlocale

import six


_trans = None


def set_language(language=None):
    global _trans
    _trans = gettext.translation(
        'l18n',
        os.path.join(os.path.dirname(__file__), 'locale'),
        languages=[language or getdefaultlocale()[0]],
        fallback=True
    )
set_language()

if six.PY2:
    def translate(s):
        return _trans.ugettext(s)
else:
    def translate(s):
        return _trans.gettext(s)


class L18NLazyString(object):

    def __init__(self, s):
        self._str = s

    def _value(self):
        return translate(self._str)

    def __str__(self):
        # needed as calling str() with an L18NLazyString actually calls
        # __repr__ if __str__ is not defined
        return self._value()

    def __repr__(self):
        return 'L18NLazyString <%s>' % self._str

    def __getattr__(self, name):
        # fallback to call the value's attribute in case it's not found in
        # L18NLazyString
        return getattr(self._value(), name)


class L18NLazyStringsList(object):

    def __init__(self, sep='/', *s):
        self._sep = sep
        self._strings = s

    def _value(self):
        return self._sep.join([translate(s) for s in self._strings])

    def __str__(self):
        return self._value()

    def __repr__(self):
        return 'L18NLazyStringsList <%s>' % self._sep.join(self._strings)

    def __getattr__(self, name):
        # fallback to call the value's attribute in case it's not found in
        # L18NLazyStringsList
        return getattr(self._value(), name)


class L18NDict(dict):

    def __getitem__(self, key):
        return L18NLazyString(super(L18NDict, self).__getitem__(key))


class L18NListDict(dict):

    def __init__(self, sep='/', *args, **kwargs):
        self._sep = sep
        super(L18NListDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        strs = key.split(self._sep)
        strs[-1] = key
        return L18NLazyStringsList(
            self._sep,
            *[super(L18NListDict, self).__getitem__(s) for s in strs]
        )

import os
import gettext
from locale import getdefaultlocale
from collections import MutableMapping

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


class L18NBaseMap(MutableMapping):
    """
    Generic dictionary that returns lazy string or lazy string lists
    """

    def __init__(self, *args, **kwargs):
        self.store = dict(*args, **kwargs)

    def __getitem__(self, key):
        raise NotImplementedError

    def _raise_readonly(self):
        raise RuntimeError('l18n maps are read-only')

    def __setitem__(self, key, value):
        self._raise_readonly()

    def __delitem__(self, key):
        self._raise_readonly()

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class L18NMap(L18NBaseMap):

    def __getitem__(self, key):
        return L18NLazyString(self.store[key])


class L18NListMap(L18NBaseMap):

    def __init__(self, sep='/', *args, **kwargs):
        self._sep = sep
        super(L18NListMap, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        strs = key.split(self._sep)
        strs[-1] = key
        return L18NLazyStringsList(self._sep, *[self.store[s] for s in strs])

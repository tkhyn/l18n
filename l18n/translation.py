import os
import gettext
from locale import getdefaultlocale
from collections import MutableMapping

import six


_trans = None


def set_language(language=None):
    global _trans
    if language:
        _trans = gettext.translation(
            'l18n',
            os.path.join(os.path.dirname(__file__), 'locale'),
            languages=[language],
            fallback=True
        )
    else:
        _trans = None
set_language(getdefaultlocale()[0])

if six.PY2:
    def translate(s, utf8=True):
        if _trans:
            if utf8:
                return _trans.ugettext(s)
            return _trans.gettext(s)
        else:
            return s
else:
    def translate(s, utf8=True):
        if _trans:
            t = _trans.gettext(s)
            if utf8:
                return t
            return t.encode()
        else:
            return s


class L18NLazyObject(object):

    def _value(self, utf8=True):
        raise NotImplementedError

    def __str__(self):
        return self._value(utf8=six.PY3)

    def __bytes__(self):
        return self._value(utf8=False)

    def __unicode__(self):
        return self._value(utf8=True)


class L18NLazyString(L18NLazyObject):

    def __init__(self, s):
        self._str = s

    def _value(self, utf8=True):
        return translate(self._str, utf8)

    def __repr__(self):
        return 'L18NLazyString <%s>' % self._str

    def __getattr__(self, name):
        # fallback to call the value's attribute in case it's not found in
        # L18NLazyString
        return getattr(self._value(), name)


class L18NLazyStringsList(L18NLazyObject):

    def __init__(self, sep='/', *s):
        # we assume that the separator and the strings have the same encoding
        # (text_type)
        self._sep = sep
        self._strings = s

    def _value(self, utf8=True):
        sep = self._sep
        if utf8 and isinstance(sep, six.binary_type):
            sep = sep.decode(encoding='utf-8')
        elif not utf8 and isinstance(sep, six.text_type):
            sep = sep.encode(encoding='utf-8')
        return sep.join([translate(s, utf8) for s in self._strings])

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

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class L18NMap(L18NBaseMap):

    def __getitem__(self, key):
        return L18NLazyString(self.store[key])


class L18NListMap(L18NBaseMap):

    def __init__(self, sep, aux=None, *args, **kwargs):
        self._sep = sep
        self._aux = aux
        super(L18NListMap, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        strs = key.split(self._sep)
        strs[-1] = key
        lst = []
        for s in strs:
            try:
                lst.append(self.store[s])
            except KeyError:
                lst.append(self._aux[s])
        return L18NLazyStringsList(self._sep, *lst)

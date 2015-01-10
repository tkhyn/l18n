l18n
====

|copyright| 2015 Thomas Khyn

Locale internationalization package. Translations for places, timezones, city
names ...

Works with Python 2.6+ and 3.3+

Supported languages: English, French (`want to add yours?`_)


What is l18n?
-------------

As you may have noticed, ``l18n`` is a contraction of ``i18n`` and ``l10n``,
namely 'internationalisation' and 'localization'. It basically provides
translations for localized names (e.g. places).

I started writing ``l18n`` when I was looking for translations for the pytz_
library. Indeed, on a multi-lingual site where users can select the timezone
they are in, it's much better if they can select in their language, as in some
cases, the differences with the english name can be significant.

And as I am lazy, I thought of a way to - almost - autmatically fetch the
translations from the CLDR_ (Unicode's Common Locale Data Repository) database.

I decided it was a good start to add other stuff, like territories codes. In
a near future, I - or contributors - may also add currencies or measurement
units ...


How does it work?
-----------------

To use ``l18n``, you first need to install it. It works well with ``pip``::

   pip install l18n

Then, in your code::

   >>> import l18n

``l18n`` exposes several read-only dictionary-like objects:

l18n.tz_locations

   is a mapping between all the timezones listed in ``pytz.common_timezones``
   to a human-friendly version of the translated name of the location
   in the current language (see `Selecting the language`_ below). For example,
   if the language is English::

      >>> l18n.tz_locations['Pacific/Easter']
      'Easter Island'

   In French, it would give::

      >>> l18n.tz_locations['Pacific/Easter']
      'Île de Pâques'

l18n.territories

   is a mapping between the territory codes as defined in the CLDR_ and their
   localized names. For example::

      >>> l18n.territories['CZ']
      'Czech Republic'  # or 'République Tchèque' in french


Selecting the language
----------------------

By default, when importing ``l18n``, the current default locale is used (via
``locale.getdefaultlocale()``). If it is not the one you want or if you need to
change it, it is rather easy::

   >>> l18n.set_language('fr')

And in case you want to go back to the default language::

   >>> l18n.set_language(None)


Versionning
-----------

``l18n``'s main version number matches ``pytz``'s version number. ``l18n``
2014.10.X will be fully compatible with ``pytz`` 2014.10 whatever the value of
X. Indeed, the primary aim is to keep ``l18n`` consistent with ``pytz``'s
updates.


Want to add a language?
-----------------------

Great idea !! Have a look at CONTRIBUTE.rst_.


Roadmap
-------

- Add supported languages
- Use an HTML parser instead of plain text lookups for data extraction
- Add currencies and other stuff


.. |copyright| unicode:: 0xA9

.. _`want to add yours?`: `Want to add a language?`
.. _pytz: https://pypi.python.org/pypi/pytz/
.. _CLDR: http://cldr.unicode.org/
.. _CONTRIBUTE.rst: https://bitbucket.org/tkhyn/l18n/src/tip/CONTRIBUTE.rst

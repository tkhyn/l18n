l18n - changes
==============


v2021.3.0 (12-11-2021)
----------------------

- add Python 3.10 support
- drop Python 2.7 support


v2020.6.1 (31-10-2020)
----------------------

- fix pytz version number

v2020.6.0 (31-10-2020)
----------------------

- fix maker encoding messages
- suppress python 3.7+ deprecated imports messages

v2018.5.0 (18-10-2018)2
----------------------

- fix installation bug on non-UTF8 platforms
- fix CLDR database archive download bug

v2016.6.4 (07-09-2016)
----------------------

- Chinese (zh) translation overrides by Charlotte Blanc
- copy/deepcopy support for l18n lazy strings and dictionaries
- fix charset bug on python 2


v2016.6.3 (30-08-2016)
----------------------

- items are now sorted in maps iterators
- subsets support


v2016.6.2 (23-08-2016)
----------------------

- fix requirement 'six'


v2016.6.1 (19-08-2016)
----------------------

- pytz 2016.6.1
- fix encoding issues


v2016.6.0 (18-07-2016)
----------------------

- pytz 2016.6
- remove strict pin against pytz version (#2)


v2016.4.0 (05-05-2016)
----------------------

- pytz 2016.4
- Czech translation overrides by Jan Čermák


v2015.7.0 (26-11-2015)
----------------------

- pytz 2015.7
- drops support for python 2.6


v2015.6.0 (15-10-2015)
----------------------

- pytz 2015.6
- German translations by Philipp Steinhardt
- Fixes locale files that were not included in some distribution targets (#1)
- Translates all pytz.all_timezones rather than only pytz.common_timezones


v2015.2.0 (22-04-2015)
----------------------

- updates pytz version to 2015.2 (no changes in translations)


v2014.10.1 (17-03-2015)
-----------------------

- Birth
- Exposes ``tz_cities``, ``tz_fullnames`` and ``territories``
  dictionary-like objects
- Compatible with python 2.6+ and 3.3+
- English and French translations

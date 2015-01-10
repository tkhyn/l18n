import re
import os
import codecs
from collections import defaultdict
from datetime import datetime
from copy import deepcopy

import pytz
import polib
import six

from .compat import configparser, unicode
from .settings import LOCALES, CLDR_TZ_CITIES_URL, CLDR_TERRITORIES_URL, \
                      PO_PATH, PY_PATH
from .helpers import get_page, log


MISSING_DIR = os.path.join(os.path.dirname(__file__), 'missing')

missing = {
    'tz_locations': defaultdict(lambda: {}),
    'territories': defaultdict(lambda: {})
}


def mk_missing():

    if any(missing.values()):
        return missing

    for locfile in os.listdir(MISSING_DIR):

        tr = configparser.ConfigParser()

        if locfile != 'en':
            tr.readfp(codecs.open(os.path.join(MISSING_DIR, 'en'),
                                  'r', 'utf8'))

        # last files override previous ones
        tr.readfp(codecs.open(os.path.join(MISSING_DIR, locfile), 'r', 'utf8'))

        for k, v in six.iteritems(missing):
            try:
                items = tr.items(k)
            except configparser.NoSectionError:
                continue
            for item, value in items:
                v[item][locfile] = value

    return missing


def mk_location_trans(tzids_list):
    """
    Generates a translation files for the given locale and the given page
    """
    current_translation = None

    # extracts the location name
    tzloc_list = []
    for tz in tzids_list:
        city = tz[tz.rfind('/') + 1:]
        tzloc_list.append([city])
        if '_' in city:
            tzloc_list[-1].append(city.replace('_', ' '))

    page = get_page(CLDR_TZ_CITIES_URL)

    log('> Processing timezone data')

    location_trans = deepcopy(mk_missing()['tz_locations'])

    not_missing = []

    for raw_line in page:

        line = unicode(raw_line)
        i = line.find(u'<th class=\'path\'>')

        if i == -1:
            if current_translation:
                # if the current city is not ignored
                i = line.find(u'<th class=\'value\'>')
                if i != -1:
                    # if the matching string for a translation is found

                    # gets the translation
                    trans = line[i + 18:line.find(u'</th>', i + 18)]

                    # remove <span> tag in the translation
                    j = trans.find(u'>')
                    if j != -1:
                        trans = trans[j + 1:trans.find(u'</span>')]

                    # go to next line
                    line = unicode(six.next(page))
                    # extract locales and remove tags
                    line = line[line.find(u'\xb7') + 1:line.rfind(u'\xb7')] \
                               .strip().replace(u'<b>', u'') \
                               .replace(u'</b>', u'').replace(u'<i>', u'') \
                               .replace(u'</i>', u'')
                    # split locales according to middle point character
                    locs = line.split(u'\xb7')

                    # browse identified locales
                    for loc in locs:
                        if loc in LOCALES and loc not in current_translation:
                            # if the locale is required, save the translation
                            current_translation[loc] = trans
        else:
            # key value
            code = re.match(".*<a name='[a-f0-9]{14,16}' "
                            "href='\\#[a-f0-9]{14,16}'>([^<]+)</a>.*",
                            line).groups()[0]

            # get only last component
            k = code.rfind('/')
            if k != -1:
                code = code[k + 1:]

            # get english translation
            en_trans = line[line.rfind(u'\u2039') + 1:line.rfind(u'\u203a')]

            try:
                k = [code in c for c in tzloc_list].index(True)
            except ValueError:
                try:
                    k = [en_trans in c for c in tzloc_list].index(True)
                except ValueError:
                    k = -1

            if k == -1:
                # default value, consider that code is not found in the tzids
                # list if neither the code or the english is in the cities
                # list, then the city is not needed and can be ignored
                current_translation = None
            else:
                # if the code or english translation matches an element in the
                # tzids list
                key = tzids_list[k]

                if key in location_trans:
                    not_missing.append((key, deepcopy(location_trans[key])))
                    if not 'en' in location_trans[key]:
                        location_trans[key]['en'] = en_trans
                else:
                    location_trans[key] = {'en': en_trans}
                current_translation = location_trans[key]

    page.close()

    if not_missing:
        log('')
        log('Some timezone translations are defined in the "missing" '
            'translation file but were actually found in the database:')
        for timezone, tr in not_missing:
            log('%s in :\n    %s' % (timezone,
                                     '\n    '.join(['%s (%s)' % i for i
                                                    in six.iteritems(tr)])))
        log('You may want to remove them from the "missing" translation files')
        log('')

    return location_trans


def mk_ter_trans(ter_dict):
    """
    Generates a translation files for the given locale and the given page
    """
    current_translation = None

    now_str = datetime.now().date().isoformat()
    cache_file_name = 'territories_' + now_str + '.htm'
    cache_file_path = os.path.join(CACHE_DIR, cache_file_name)

    page = get_page(CLDR_TERRITORIES_URL)

    log('> Processing territories data')

    ter_trans = deepcopy(mk_missing()['territories'])
    not_missing = []

    for raw_line in page:

        line = unicode(raw_line)
        i = line.find(u'<th class=\'path\'>')

        if i == -1:
            if current_translation:
                # if the current city is not ignored
                i = line.find(u'<th class=\'value\'>')
                if i != -1:
                    # if the matching string for a translation is found

                    # gets the translation
                    trans = line[i + 18:line.find(u'</th>', i + 18)]
                    # remove <span> tag in the translation
                    j = trans.find(u'>')
                    if j != -1:
                        trans = trans[j + 1:trans.find(u'</span>')]

                    # go to next line
                    line = unicode(six.next(page))
                    # extract locales and remove tags
                    line = line[line.find(u'\xb7') + 1:line.rfind(u'\xb7')] \
                               .strip().replace(u'<b>', u'') \
                               .replace(u'</b>', u'').replace(u'<i>', u'') \
                               .replace(u'</i>', u'')
                    # split locales according to middle point character
                    locs = line.split(u'\xb7')

                    # browse identified locales
                    for loc in locs:
                        if loc in LOCALES and loc not in current_translation:
                            # if the locale is required, save the translation
                            current_translation[loc] = trans

        else:
            # key value
            code = re.match(".*<a name='[a-f0-9]{14,16}' "
                            "href='\\#[a-f0-9]{14,16}'>([^<]+)</a>.*",
                            line).groups()[0]

            # get english translation
            en_trans = line[line.rfind(u'\u2039') + 1:line.rfind(u'\u203a')]

            default = ter_dict.get(code, None)

            if default == None:
                # not found
                current_translation = None
            else:
                # found, set english translation and current dictionnary entry
                if code in ter_trans:
                    not_missing.append((code, deepcopy(ter_trans[code])))
                    if 'en' not in ter_trans:
                        ter_trans[code] = en_trans
                else:
                    ter_trans[code] = {'en': en_trans}
                current_translation = ter_trans[code]

    page.close()

    if not_missing:
        log('')
        log('Some territories translations are defined in the "missing" '
            'translation file but were actually found in the database:')
        for territory, tr in six.iteritems(not_missing):
            log('%s in :\n    %s' % (territory,
                                     '\n    '.join(['%s (%s)' % i for i
                                                    in six.iteritems(tr)])))
        log('You may want to remove them from the "missing" translation files')
        log('')

    return ter_trans


def mk_py(tzids_list, location_trans, ter_dict, ter_trans):
    """
    Generate .py file with a dict of default (english) values
    """

    log('> Generating __maps.py with default (english) values')

    py_file = codecs.open(PY_PATH, 'w', ' utf8')
    py_file.write('# -*- coding: utf-8 -*-\n\n'
                  '# AUTOMATICALLY GENERATED FILE, DO NOT EDIT\n\n'
                  'tz_locations = {\n')

    # cities
    cit_defaults = list()
    not_found = []
    for tz in tzids_list:
        # browse list
        if location_trans.get(tz, None):
            # if a translation exists, save the english in defaults
            cit_defaults.append(location_trans[tz]['en'])
        else:
            # if not, save city name and displays a warning
            cit_defaults.append(tz[tz.rfind('/') + 1:])
            not_found.append(tz)
        # write default translation in py file
        py_file.write(u"    '%s': u'%s',\n"
                      % (tz, cit_defaults[-1].replace(u"'", u"\\'")))

    if not_found:
        log('')
        log('Warning: no translation entry found for the following tzs:')
        for tz in not_found:
            print(tz)
        log('You may want to append them to the appropriate locale file(s) in '
            'the "missing" directory')
        log('')

    py_file.write('}')

    # territory names
    not_found = []
    py_file.write('\n\nterritories = {\n')
    for (k, d) in six.iteritems(ter_dict):
        # browse list
        if ter_trans.get(k, None):
            # if a translation exists, save the english in defaults
            ter_dict[k] = ter_trans[k]['en']
        else:
            # if not, don't change anything and add to not_found list
            not_found.append((d, k))
        # write default translation in py file
        py_file.write(u"    '%s': u'%s',\n"
                      % (k, ter_dict[k].replace(u"'", u"\\'")))

    if not_found:
        log('')
        log('Warning: no translation entry found for the following '
            'territories:')
        for t, k in not_found:
            print('%s (%s)' % (k, t))
        log('You may want to append them to the appropriate locale file(s) in '
            'the "missing" directory')
        log('')

    py_file.write('}\n')

    # close file
    py_file.close()

    return cit_defaults


def mk_po(loc, tzids_list, cit_defaults, location_trans, ter_dict, ter_trans):
    """
    Generate a .po file for locale loc
    """

    header = u"""# PYTZ TIMEZONE CITIES AND TERRITORIES TRANSLATION FILE

msgid ""
msgstr ""

"Project-Id-Version: l18n\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: %(date)s\\n"
"PO-Revision-Date: \\n"
"Last-Translator: l18n maker\\n"
"Language-Team: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n > 1)\\n"
"X-Poedit-SourceCharset: utf-8\\n"
"Language: """ % {'date': datetime.now(pytz.utc).replace(microsecond=0)}

    log('> Generating .po file for locale ' + loc)

    po_path = PO_PATH % loc
    try:
        os.makedirs(os.path.dirname(po_path))
    except OSError:
        pass

    po_file = codecs.open(po_path, 'w', ' utf8')
    po_file.write(header + loc + u'\\n"\n\n')
    # cities
    written = list()
    for tz, default in zip(tzids_list, cit_defaults):
        t = location_trans.get(tz, None)
        if t and t.get(loc, None) and (not t[loc] == default) \
        and (default not in written):
                written.append(default)
                po_file.write(u'msgid "' + default + u'"\nmsgstr "' +
                              t[loc] + u'"\n\n')
    # territories
    for t, default in six.iteritems(ter_dict):
        ttr = ter_trans.get(t, None)
        if ttr and ttr.get(loc, None) and (not ttr[loc] == default) \
        and (default not in written):
            written.append(default)
            po_file.write(u'msgid "' + default + u'"\nmsgstr "' +
                          ttr[loc] + u'"\n\n')
    po_file.close()
    return po_path


def mk_mo(po_path):
    polib.pofile(po_path).save_as_mofile(po_path[:-3] + '.mo')


def mk_trans():

    log('Starting cities and territories names translation')

    try:
        os.makedirs(CACHE_DIR)
    except OSError:
        # directory exists
        pass

    tzids_list = pytz.common_timezones
    location_trans = mk_location_trans(tzids_list)

    ter_dict = dict()
    for (k, i) in six.iteritems(pytz.country_names):
        if pytz.country_timezones.get(k, None):
            # make a dictionary entry only if there is at least 1 timezone
            # in the country
            ter_dict[k] = i
    ter_trans = mk_ter_trans(ter_dict)

    cit_defaults = mk_py(tzids_list, location_trans, ter_dict, ter_trans)

    for loc in LOCALES:
        if loc == 'en':
            # no need to generate a translation file for english
            continue
        po_path = mk_po(loc, tzids_list, cit_defaults, location_trans,
                        ter_dict, ter_trans)
        mk_mo(po_path)

    log('Cities and territories names translation completed')

    return 0

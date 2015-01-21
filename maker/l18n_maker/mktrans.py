import os
import codecs
from collections import defaultdict
from datetime import datetime
from copy import deepcopy
import re

import pytz
import polib
import six
from lxml import etree as ET

from .compat import configparser
from .settings import LOCALES, PO_PATH, PY_PATH
from .helpers import get_data_dir, log


MISSING_DIR = os.path.join(os.path.dirname(__file__), 'missing')

ITEMS = ('tz_locations', 'tz_cities', 'territories')

missing = defaultdict(lambda: dict([(i, {}) for i in ITEMS]))


def mk_missing():

    if any(missing.values()):
        return missing

    for locfile in os.listdir(MISSING_DIR):

        tr = configparser.ConfigParser()
        tr.readfp(codecs.open(os.path.join(MISSING_DIR, locfile), 'r', 'utf8'))

        for i in ITEMS:
            try:
                items = tr.items(i)
            except configparser.NoSectionError:
                continue
            for item, value in items:
                missing[locfile][i][item] = value

    return missing


def mk_locale_trans(loc, defaults=None):

    if defaults is None:
        defaults = defaultdict(lambda: {})

    trans_dict = deepcopy(mk_missing()[loc])
    missing = defaultdict(lambda: [])
    not_missing_overrides = defaultdict(lambda: [])
    not_missing_same = defaultdict(lambda: [])


    def save_trans(name, key, trans, store_not_missing=True):
        cur_trans = trans_dict[name].get(key, None)
        if cur_trans and store_not_missing:
            # a translation is already defined
            if cur_trans == trans:
                not_missing_same[name].append(key)
            else:
                not_missing_overrides[name].append((trans, cur_trans))
        else:
            # no existing translation is defined, save it if different than
            # default value
            if trans != defaults[name].get(key, None):
                trans_dict[name][key] = trans

    # there are no territories defined in root.xml, so the default ones should
    # be extracted from en.xml
    ldml = ET.parse(os.path.join(get_data_dir(), 'main', '%s.xml'
                                 % ('en' if loc == 'root' else loc))).getroot()

    ter_required = set(pytz.country_names.keys()) \
                       .difference(defaults['territories'].keys())
    for territory in ldml.find('localeDisplayNames').find('territories'):
        if territory.tag != 'territory' \
        or territory.get('alt', None) is not None:
            continue
        key = territory.get('type')
        save_trans('territories', key, territory.text)
        try:
            ter_required.remove(key)
        except KeyError:
            pass
    missing['territories'].extend(ter_required)


    if loc == 'root':
        # back to root.xml for timezones
        ldml = ET.parse(os.path.join(get_data_dir(), 'main',
                                     'root.xml')).getroot()

    tz_required = set(pytz.common_timezones) \
                      .difference(defaults['tz_cities'].keys())
    for zone in ldml.find('dates').find('timeZoneNames'):
        if zone.tag != 'zone':
            continue

        key = zone.get('type')
        try:
            tz_required.remove(key)
        except KeyError:
            if key not in pytz.common_timezones:
                continue

        ex_city = zone.find('exemplarCity')
        if ex_city is None:
            city = key.split('/')[-1].replace('_', ' ')
        else:
            # stripping territory name in cases like 'city [territory]' or
            # 'city, territory'
            city = re.sub('(?:, .*| \[.*\])$', '', ex_city.text)
        save_trans('tz_cities', key, city)

        for location in set(key.split('/')[:-1]):
            if location in (trans_dict['tz_locations'].keys() +
                            missing['tz_locations']):
                continue
            if loc == 'root':
                missing['tz_locations'].append(location)
            save_trans('tz_locations', location, location.replace('_', ' '))

    if loc == 'root':
        # populate missing default translations with raw city names
        for zone in tz_required:
            zone_split = zone.split('/')
            save_trans('tz_cities', zone, zone_split[-1].replace('_', ' '),
                       store_not_missing=False)

            for location in set(zone_split[:-1]):
                if location in (trans_dict['tz_locations'].keys() +
                                missing['tz_locations']):
                    continue
                missing['tz_locations'].append(location)
                save_trans('tz_locations', location,
                           location.replace('_', ' '))
    else:
        # report missing translations
        missing['tz_cities'].extend(tz_required)

    return trans_dict, missing, not_missing_overrides, not_missing_same


def mk_py(trans):
    """
    Generate .py file with a dict of default (english) values
    """

    log('> Generating __maps.py with default (english) values')

    py_file = codecs.open(PY_PATH, 'w', ' utf8')
    py_file.write('# -*- coding: utf-8 -*-\n\n'
                  '# AUTOMATICALLY GENERATED FILE, DO NOT EDIT')

    def write(name):
        py_file.write('\n\n%s = {\n' % name)
        for k, v in six.iteritems(trans[name]):
            py_file.write(u"    '%s': u'%s',\n" % (k, v.replace(u"'", u"\\'")))
        py_file.write('}')

    for name in ITEMS:
        write(name)

    # close file
    py_file.close()


def mk_po(loc, trans_en, trans):
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

    def write(name):
        for k, v in six.iteritems(trans[name]):
            po_file.write(u'msgid "' + trans_en[name][k] + \
                          u'"\nmsgstr "' + v + u'"\n\n')

    for name in ITEMS:
        write(name)

    po_file.close()
    return po_path


def mk_mo(po_path):
    polib.pofile(po_path).save_as_mofile(po_path[:-3] + '.mo')


def mk_trans():

    log('Starting cities and territories names translation')

    # translations, missing, overriden in 'missing' folder, same value in
    # missing folder
    result = [{}, {}, {}, {}]

    defaults = None
    for loc in ('root',) + LOCALES:
        for i, r in enumerate(mk_locale_trans(loc, defaults)):
            if any(r.values()):
                result[i][loc] = r
                if loc == 'root' and i == 0:
                    defaults = r

    for res, msg, post_msg in zip(
        result[1:],
        ('Some translations are missing',
         'Some translations were overriden by entries in "missing" files',
         'Some translation overrides are no longer useful'),
        ('You may want to add them in files in the "missing" directory',
         None,
         'You may want to remove them from the "missing" translation files')):

        if res:
            log('')
            log(msg)
            for loc, dic in six.iteritems(res):
                for name, ids in six.iteritems(dic):
                    if not ids:
                        continue
                    if isinstance(ids[0], six.string_types):
                        to_join = ids
                    else:
                        # ids is a list of doubles
                        to_join = ['"%s" (by "%s")' % x for x in ids]
                    log('- %s / %s: %s' % (loc, name, ', '.join(to_join)))
            if post_msg:
                log(post_msg)
            log('')


    trans = result[0]

    trans_root = trans['root']
    mk_py(trans_root)

    for loc in LOCALES:
        po_path = mk_po(loc, trans_root, trans[loc])
        mk_mo(po_path)

    log('Cities and territories names translation completed')

    return 0

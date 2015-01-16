from __future__ import print_function

import os
import codecs
from datetime import datetime
import re

from bs4 import BeautifulSoup, FeatureNotFound

from .compat import urllib2


CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')


def unicode_url(url):

    ctnt = urllib2.urlopen(url).read()

    uctnt = unicode(ctnt, 'utf-8')
    line = ''
    i = 0
    j = 0

    while j > -1:
        j = uctnt.find(u'\n', i)
        line = uctnt[i:j]
        i = j + 1
        yield line
    return


def get_page(url):
    """
    Retrieves a page from an URL and cache it
    """

    try:
        os.makedirs(CACHE_DIR)
    except OSError:
        # directory exists
        pass

    now_str = datetime.now().date().isoformat()
    cache_file_name, ext = os.path.splitext(url.split('/')[-1])
    cache_file_name += '_' + now_str + ext
    cache_file_path = os.path.join(CACHE_DIR, cache_file_name)

    try:
        page = codecs.open(cache_file_path, 'r', ' utf8')
        log('> Loading page from file (%s)' % cache_file_name)
    except IOError:
        log('> Retrieving page from CLDR website')
        html = unicode_url(url)
        page = codecs.open(cache_file_path, 'w', ' utf8')
        # fixing a tr tag HTML bug on CLDR pages
        page.writelines([re.sub('</t([dh])><tr>', '</t\\1></tr>', l) + u'\n'
                         for l in html])
        page.close()
        log('> Page saved to %s' % cache_file_name)
        page = codecs.open(cache_file_path, 'r', ' utf8')

    html = page.read()

    log('> Parsing HTML with BeautifulSoup')
    try:
        bs_page = BeautifulSoup(html, 'lxml')
    except FeatureNotFound:
        log('> WARNING: lxml is not installed, HTML parsing will be '
            'very slow')
        bs_page = BeautifulSoup(html)
    page.close()

    return bs_page


def log(msg):
    print(msg)

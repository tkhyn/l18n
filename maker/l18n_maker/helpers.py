from __future__ import print_function

import os
import codecs
from datetime import datetime

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
    now_str = datetime.now().date().isoformat()
    cache_file_name, ext = os.path.splitext(url.split('/')[-1].split('.'))
    cache_file_name += '_' + now_str + ext
    cache_file_path = os.path.join(CACHE_DIR, cache_file_name)

    try:
        page = codecs.open(cache_file_path, 'r', ' utf8')
        log('> Loading timezone data from file (%s)' % cache_file_name)
    except IOError:
        log('> Getting timezone data from CLDR website (saving it in %s)'
            % cache_file_name)
        html = unicode_url(url)
        page = codecs.open(cache_file_path, 'w', ' utf8')
        page.writelines([(l + u'\n') for l in html])
        page.close()
        page = codecs.open(cache_file_path, 'r', ' utf8')



def log(msg):
    print(msg)

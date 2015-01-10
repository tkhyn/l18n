from __future__ import print_function

from .compat import urllib2


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


def log(msg):
    print(msg)

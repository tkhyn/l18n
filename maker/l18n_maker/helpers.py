from __future__ import print_function

import os
import zipfile
import StringIO

import requests

from .settings import CLDR_DATA_URL

DATA_DIR = os.path.join(os.path.dirname(__file__), 'cldr_db')


_get_data_dir_called = False


def get_data_dir():
    """
    Retrieves the latest CLDR database, unzip and saves it, returns the version
    """
    global _get_data_dir_called

    request = requests.get(CLDR_DATA_URL)

    version = request.url.split('/')[-2]

    data_dir = os.path.join(DATA_DIR, version)

    if os.path.exists(data_dir):
        if not _get_data_dir_called:
            log('> Loading data from cached database (%s)' % data_dir)
    else:
        try:
            os.makedirs(data_dir)
        except OSError:
            pass  # DATA_DIR exists
        log('> Downloading CLDR database version %s' % version)
        request = requests.get(CLDR_DATA_URL + '/core.zip')
        z = zipfile.ZipFile(StringIO.StringIO(request.content))
        log('> Extracting CLDR database to %s' % data_dir)
        z.extractall(data_dir)

    _get_data_dir_called = True
    return os.path.join(data_dir, 'common')


def log(msg):
    print(msg.encode('utf-8'))

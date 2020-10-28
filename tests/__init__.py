from __future__ import print_function

import os
import sys
import shutil

from .compat import reload
from .maker import build


sys.path.append(os.sep.join(__file__.split(os.sep)[:-2] + ['maker']))

from l18n_maker.settings import LOCALE_PATH, PY_PATH

orig_paths = (LOCALE_PATH, PY_PATH)
backup_paths = [o + '.bak' for o in orig_paths]


def setUp():
    # generates the .po and .mo files
    # this will raise an exception and cancel the test run

    print('Generating test .po and .mo files ... ', end='', file=sys.stderr)

    try:
        # backup existing locale folder if any
        for o, b in zip(orig_paths, backup_paths):
            try:
                os.rename(o, b)
            except OSError:
                pass

        build()

        for m in ('l18n.__maps', 'l18n.maps', 'l18n'):
            try:
                reload(sys.modules[m])
            except (KeyError, ImportError):
                pass
        print('Done', file=sys.stderr)
    except:
        tearDown()
        raise


def tearDown():

    # cleanup
    try:
        shutil.rmtree(LOCALE_PATH)
        os.remove(PY_PATH)
    except OSError:
        pass

    # restore backed up existing locale folder if any

    # backup existing locale folder if any
    for o, b in zip(orig_paths, backup_paths):
        try:
            os.rename(b, o)
        except OSError:
            pass

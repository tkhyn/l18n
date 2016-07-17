"""
l18n
Locale internationalization package
(c) 2015 Thomas Khyn and contributors (see CONTRIBUTORS.rst)
MIT License (see LICENSE.txt)
"""

import os
import sys

from setuptools import setup
from distutils import log

import subprocess


# imports __version__ variable
exec(open('l18n/version.py').read())
dev_status = __version_info__[3]

if dev_status == 'alpha' and not __version_info__[4]:
    dev_status = 'pre'

DEV_STATUS = {'pre': '2 - Pre-Alpha',
              'alpha': '3 - Alpha',
              'beta': '4 - Beta',
              'rc': '4 - Beta',
              'final': '5 - Production/Stable'}


class PredistBuild(object):
    """
    Mixin class to build translation files
    """
    def build_trans(self):
        log.info('building translation files')

        # we need to use buildout, call the following commands in the specified
        # order, and reverse if an issue is raised
        cmds = [[os.path.join('bin', 'build')],
                [os.path.join('bin', 'buildout'), 'parts=build'],
                ['python', 'bootstrap.py']]
        cmd = 0

        try:
            from subprocess import DEVNULL
        except ImportError:
            DEVNULL = open(os.devnull, 'wb')

        while True:
            try:
                log.info('    - calling "%s"' % ' '.join(cmds[cmd]))
                if subprocess.Popen(cmds[cmd], stderr=DEVNULL,
                                    stdout=DEVNULL).wait():
                    raise OSError
                if not cmd:
                    break
                else:
                    cmd -= 1
            except OSError:
                cmd += 1
                if cmd > 2:
                    if os.path.exists(os.path.join(os.path.dirname(__file__),
                                                   'l18n', '__maps.py')):
                        break
                    else:
                        raise RuntimeError('Could not build translation files')

        log.info('translation files built successfully')

cmd_classes = {}
for cmd in ('sdist', 'bdist', 'bdist_egg', 'bdist_rpm', 'bdist_wininst'):
    try:
        cmd_module = getattr(__import__('setuptools.command', fromlist=[cmd]),
                             cmd)
    except (AttributeError, ImportError):
        # That's a distutils command (bdist)
        cmd_module = getattr(__import__('distutils.command', fromlist=[cmd]),
                             cmd)

    base_class = getattr(cmd_module, cmd)

    def get_run(base_class):
        def run(self):
            self.build_trans()
            return base_class.run(self)
        return run

    cmd_classes[cmd] = type(cmd + '_build', (base_class, PredistBuild), {
        'run': get_run(base_class)
    })


# setup function parameters
setup(
    name='l18n',
    version=__version__,
    description='Internationalization for pytz timezones and territories',
    long_description=open(os.path.join('README.rst')).read(),
    author='Thomas Khyn',
    author_email='thomas@ksytek.com',
    url='https://bitbucket.org/tkhyn/l18n',
    keywords=['pytz', 'translation', 'i18n'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'Topic :: Software Development :: Internationalization'
    ],
    packages=('l18n',),
    install_requires=('pytz>=%d.%d' % __version_info__[:2],),
    cmdclass=cmd_classes,
    zip_safe=False,
    include_package_data=True,
)

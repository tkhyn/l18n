"""
l18n
Locale internationalization package
(c) 2015 Thomas Khyn and contributors (see CONTRIBUTORS.rst)
MIT License (see LICENSE.txt)
"""

from setuptools import setup
import os


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
        'Programming Language :: Python 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'Topic :: Software Development :: Internationalization'
    ],
    packages=('l18n',),
    install_requires=('pytz==%d.%d' % __version_info__[:2])
)

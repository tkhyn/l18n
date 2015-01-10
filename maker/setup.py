"""
l18n maker script
"""

from setuptools import setup

exec(open('../l18n/version.py').read())

setup(
    name='l18n_maker',
    packages=('l18n_maker',),
    entry_points={
        'console_scripts': [
            'build=l18n_maker:build',
        ],
    },
    install_requires=(
        'pytz==%d.%d' % __version_info__[:2],
        'polib',
        'six'
    ),
)

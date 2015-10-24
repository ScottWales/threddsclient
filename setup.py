#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

def changes():
    with open('CHANGES.rst') as f:
        return f.read()


setup(name             = 'threddsclient',
      version          = '0.3.3',
      description      = 'Thredds catalog client',
      long_description = readme() + '/n/n' + changes(),
      author	       = 'Birdhouse',
      email            = '',
      license          = 'Apache 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe         = False,
      install_requires =
      ['requests',
       'beautifulsoup4',
       'lxml',
       'pytest',
       ],
      )

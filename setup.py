#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

def changes():
    with open('CHANGES.md') as f:
        return f.read()


setup(name             = 'threddsclient',
      version          = '0.3.1',
      description      = 'Thredds catalog client',
      long_description = readme() + '/n/n' + changes(),
      author	       = 'Birdhouse',
      license          = 'Apache 2.0',
      packages         = ['threddsclient'],
      zip_safe         = False,
      install_requires =
      ['requests',
       'beautifulsoup4',
       'lxml',
       'pytest',
       ],
      )

#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

reqs = [line.strip() for line in open('requirements.txt')]

setup(name             = 'threddsclient',
      version          = '0.3.4',
      description      = 'Thredds catalog client',
      long_description = long_description,
      author	       = 'Birdhouse',
      email            = '',
      license          = 'Apache 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe         = False,
      install_requires = reqs,
      )

#!/usr/bin/env python

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
        name             = 'threddsclient',
        version          = '0.1.0',
        description      = 'Thredds catalog client',
        long_description = readme(),
        author           = 'Scott Wales',
        author_email     = 'scott.wales@unimelb.edu.au',
        license          = 'Apache 2.0',
        packages         = ['threddsclient'],
        zip_safe         = False,
        install_requires = [
            'requests',
            'beautifulsoup4',
            ],
        )

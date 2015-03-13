#!/usr/bin/env python
"""
A Python view of a Thredds data server

author: Scott Wales <scott.wales@unimelb.edu.au>

Copyright 2015 ARC Centre of Excellence for Climate Systems Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from bs4 import BeautifulSoup as BSoup
import requests
import urlparse

from .nodes import *


def readUrl(url, **kwargs):
    """
    Create a Catalog from a Thredds catalog link

    :param str url:     URL pointing to a Thredds catalog.xml file
    :param \**kwargs:   Arguments to pass to requests.get()
                        (e.g. for authentication)
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    :raises requests.ConnectionError: if unable to connect to the URL
    """
    req = requests.get(url, **kwargs)
    readXml(req.text, url)


def readXml(xml, baseurl):
    """
    Create a Catalog from a XML string

    :param str xml:     XML code for a Thredds catalog
    :param str baseurl: URL base to use for catalog links
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    """
    try:
        soup = BSoup(xml, 'xml').catalog
        soup.name  # Xml should contain <catalog/> at top level
    except AttributeError:
        raise ValueError("Does not appear to be a Thredds catalog")

    catalog = Catalog()
    catalog.name = soup.get('name')

    # Collect references and datasets
    catalog.services = [Service(x, baseurl) for x in
                        soup.find_all('service', recursive=False)]
    catalog.references = [Reference(x, baseurl) for x in
                          soup.find_all('catalogRef', recursive=False)]
    catalog.datasets = [Dataset(x) for x in
                        soup.find_all('dataset', recursive=False)]

    return catalog


class Catalog:
    "A Thredds catalog entry"
    def __init__(self):
        self.name = ""
        self.services = []
        self.references = []
        self.datasets = []

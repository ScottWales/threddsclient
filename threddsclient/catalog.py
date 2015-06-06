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
import re

from .nodes import Service, Reference, Dataset

import logging
logger = logging.getLogger(__name__)

SKIPS = [".*files.*", ".*Individual Files.*", ".*File_Access.*", ".*Forecast Model Run.*", ".*Constant Forecast Offset.*", ".*Constant Forecast Date.*", "\..*"]

def readUrl(url, skip=None, **kwargs):
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
    return readXml(req.text, url)


def readXml(xml, baseurl, skip=None):
    """
    Create a Catalog from a XML string

    :param str xml:     XML code for a Thredds catalog
    :param str baseurl: URL base to use for catalog links
    :param str skip:        list of dataset names and/or a catalogRef titles.  Python regex supported.
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    """
    try:
        soup = BSoup(xml, 'xml').catalog
        soup.name  # Xml should contain <catalog/> at top level
    except AttributeError:
        raise ValueError("Does not appear to be a Thredds catalog")

    # Skip these dataset links, such as a list of files
    # ie. "files/"
    if skip is None:
        skip = SKIPS
    skip = map(lambda x: re.compile(x), skip)

    catalog = Catalog()
    catalog.name = soup.get('name')

    # Collect references and datasets
    catalog.services = [Service(x, baseurl) for x in
                        soup.find_all('service', recursive=False)]

    catalog.references = []
    for ref in soup.find_all('catalogRef', recursive=True):
        title = ref.get('xlink:title', '')
        if any([x.match(title) for x in skip]):
            logger.info("Skipping catalogRef based on 'skips'.  Title: %s" % title)
            continue
        else:
            catalog.references.append(Reference(ref, baseurl))

    catalog.datasets = []
    for ds in soup.find_all('dataset', recursive=True):    
        name = ds.get("name")
        if any([x.match(name) for x in skip]):
            logger.info("Skipping dataset based on 'skips'.  Name: %s" % name)
            continue
        elif ds.get('urlPath') is None:
            logger.debug("Skipping dataset with no urlPath.  Name: %s" % name)
            continue
        else:
            catalog.datasets.append( Dataset(ds, catalog.services) )

    return catalog

def download_urls(url, recursive=False):
    catalog = readUrl(url)
    urls = []
    for dataset in catalog.datasets:
        urls.append(dataset.fileurl())
    return urls

class Catalog:
    "A Thredds catalog entry"
    def __init__(self):
        self.name = ""
        self.services = []
        self.references = []
        self.datasets = []

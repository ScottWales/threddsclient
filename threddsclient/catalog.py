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

from .nodes import Service, CatalogRef, CollectionDataset, DirectDataset

import logging
logger = logging.getLogger(__name__)

SKIPS = [".*files.*", ".*Individual Files.*", ".*File_Access.*", ".*Forecast Model Run.*", ".*Constant Forecast Offset.*", ".*Constant Forecast Date.*", "\..*"]

def read_url(url, skip=None, **kwargs):
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
    return read_xml(req.text, url)


def read_xml(xml, baseurl, skip=None):
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

    catalog = Catalog()
    catalog.name = soup.get('name')
    
    skip = skip_pattern(skip)

    # Collect datasets
    catalog.services = find_services(soup, baseurl)
    catalog.references = find_references(soup, baseurl, skip)
    catalog.datasets = find_datasets(soup, baseurl, catalog, skip)
    return catalog

def skip_pattern(skip=None):
    # Skip these dataset links, such as a list of files
    # ie. "files/"
    if skip is None:
        skip = SKIPS
    skip = map(lambda x: re.compile(x), skip)
    return skip

def find_services(soup, baseurl):
    return [Service(x, baseurl) for x in soup.find_all('service', recursive=False)]

def find_references(soup, baseurl, skip):
    references = []
    for ref in soup.find_all('catalogRef', recursive=False):
        title = ref.get('xlink:title', '')
        if any([x.match(title) for x in skip]):
            logger.info("Skipping catalogRef based on 'skips'.  Title: {0}".format(title))
            continue
        else:
            references.append(CatalogRef(ref, baseurl))
    return references

def find_datasets(soup, baseurl, catalog, skip):
    datasets = []
    for ds in soup.find_all('dataset', recursive=False):    
        name = ds.get("name")
        if any([x.match(name) for x in skip]):
            logger.info("Skipping dataset based on 'skips'.  Name: {0}".format(name))
            continue
        elif ds.get('urlPath') is None:
            datasets.append( CollectionDataset(ds, baseurl, catalog, skip) )
        else:
            datasets.append( DirectDataset(ds, baseurl, catalog) )
    return datasets

def download_urls(url, recursive=False):
    catalog = read_url(url)
    return catalog.download_urls(recursive)

def flat_datasets(datasets):
    flat_ds = []
    for ds in datasets:
        if ds.is_collection():
            flat_ds.extend(flat_datasets(ds.datasets))
        else:
            flat_ds.append(ds)
    return flat_ds

def flat_references(datasets):
    flat_refs = []
    for ds in datasets:
        if ds.is_collection():
            flat_refs.extend(ds.references)
            flat_refs.extend(flat_references(ds.datasets))
    return flat_refs

class Catalog:
    "A Thredds catalog entry"
    def __init__(self):
        self.name = ""
        self.services = []
        self.references = []
        self.datasets = []

    def flat_datasets(self):
        return flat_datasets(self.datasets)

    def flat_references(self):
        flat_refs = []
        flat_refs.extend(self.references)
        flat_refs.extend(flat_references(self.datasets))
        return flat_refs

    def download_urls(self, recursive=False):
        urls = []
        for dataset in self.flat_datasets():
            urls.append(dataset.fileurl())
        return urls

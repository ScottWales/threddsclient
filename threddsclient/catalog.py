"""
A Python view of a Thredds data server

http://www.unidata.ucar.edu/software/thredds/current/tds/tutorial/CatalogPrimer.html
"""

from bs4 import BeautifulSoup as BSoup
import requests

from threddsclient import utils

import logging
logger = logging.getLogger(__name__)


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

    catalog = Catalog(baseurl)
    catalog.name = soup.get('name')
       
    skip = utils.skip_pattern(skip)
    
    # Collect datasets
    catalog.services = utils.find_services(soup, catalog)
    catalog.references = utils.find_references(soup, catalog, skip)
    catalog.datasets = utils.find_datasets(soup, catalog, skip)
    
    return catalog

def download_urls(url, recursive=False):
    catalog = read_url(url)
    return catalog.download_urls(recursive)

class Catalog:
    "A Thredds catalog entry"
    def __init__(self, url):
        self.url = url
        self.name = ""
        self.services = []
        self.references = []
        self.datasets = []

    def flat_datasets(self):
        return utils.flat_datasets(self.datasets)

    def flat_references(self):
        flat_refs = []
        flat_refs.extend(self.references)
        flat_refs.extend(utils.flat_references(self.datasets))
        return flat_refs

    def download_urls(self, recursive=False):
        urls = []
        for dataset in self.flat_datasets():
            urls.append(dataset.fileurl())
        return urls

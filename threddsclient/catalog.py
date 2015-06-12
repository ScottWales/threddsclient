"""
A Python view of a Thredds data server

http://www.unidata.ucar.edu/software/thredds/current/tds/tutorial/CatalogPrimer.html
"""

from threddsclient import utils

import logging
logger = logging.getLogger(__name__)


def download_urls(url, recursive=False):
    catalog = read_url(url)
    return catalog.download_urls(recursive)

class Catalog:
    "A Thredds catalog"
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.name = ""
        self._services = None
        self.references = []
        self.datasets = []

    @property
    def services(self):
        if not self._services:
            from .nodes import Service
            self._services = [Service(x, self) for x in self.soup.find_all('service', recursive=False)]
        return self._services

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

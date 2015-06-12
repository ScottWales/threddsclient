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

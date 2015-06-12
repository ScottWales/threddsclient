"""
A Python view of a Thredds data server

http://www.unidata.ucar.edu/software/thredds/current/tds/tutorial/CatalogPrimer.html
"""

import logging
logger = logging.getLogger(__name__)


SKIPS = [".*files.*", ".*Individual Files.*", ".*File_Access.*", ".*Forecast Model Run.*", ".*Constant Forecast Offset.*", ".*Constant Forecast Date.*", "\..*"]


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


def skip_pattern(skip=None):
    # Skip these dataset links, such as a list of files
    # ie. "files/"
    import re
    if skip is None:
        skip = SKIPS
    skip = map(lambda x: re.compile(x), skip)
    return skip

class Catalog:
    "A Thredds catalog"
    def __init__(self, soup, url, skip=None):
        self.soup = soup
        self.url = url
        self.skip = skip_pattern(skip)
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



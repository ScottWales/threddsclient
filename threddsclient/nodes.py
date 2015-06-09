"""
A Python view of a Thredds data server
"""

from bs4 import BeautifulSoup as BSoup
import urlparse
from .utils import size_in_bytes

import logging
logger = logging.getLogger(__name__)

class Node:
    """
    Common items to all nodes
    """
    def __init__(self, soup, catalog):
        self.catalog = catalog
        self.name = soup.get('name')
        self.content_type = None
        self.bytes = None
        self.modified = None

    def __repr__(self):
        return "<Node name: {0.name}, content type: {0.content_type}>".format(self)


class Service(Node):
    """
    A Thredds service
    """
    def __init__(self, soup, catalog):
        Node.__init__(self, soup, catalog)
        self.base = soup.get('base')
        self.url = urlparse.urljoin(self.catalog.url, self.base)
        self.service_type = soup.get('serviceType')
        self.content_type = "application/service"
        self.services = [Service(s, self.catalog) for s in soup.find_all('service', recursive=False)]

class CatalogRef(Node):
    """
    A reference to a different Thredds catalog
    """
    def __init__(self, soup, catalog):
        Node.__init__(self, soup, catalog)
        self.title = soup.get('xlink:title')
        self.name = self.title
        self.href = soup.get('xlink:href')
        self.url = urlparse.urljoin(self.catalog.url, self.href)
        self.content_type = "application/directory"

    def follow(self):
        from .catalog import read_url
        return read_url(self.url)

class Dataset(Node):
    """
    Abstract dataset class
    """
    def __init__(self, soup, catalog):
        Node.__init__(self, soup, catalog)
        self.ID = soup.get('ID')
        self.url = "{0}?dataset={1}".format(self.catalog.url, self.ID)

    def is_collection(self):
        return False
    
class CollectionDataset(Dataset):
    """
    A container for other datasets
    """
    def __init__(self, soup, catalog, skip=[]):
        Dataset.__init__(self, soup, catalog)
        self.content_type = "application/directory"
        from .utils import find_datasets
        self.datasets = find_datasets(soup, self.catalog, skip)
        from .utils import find_references
        self.references = find_references(soup, self.catalog, skip)

    def is_collection(self):
        return True
        
class DirectDataset(Dataset):
    """
    A reference to a data file
    """
    def __init__(self, soup, catalog):
        Dataset.__init__(self, soup, catalog)
        self.url_path = soup.get('urlPath')
        self.content_type = "application/netcdf"
        self.modified = self._modified(soup)
        self.bytes = self._bytes(soup)
        self.service_name = self._service_name(soup)

    def fileurl(self):
        for service in self.catalog.services[0].services:
            if service.service_type == "HTTPServer":
                return urlparse.urljoin(service.url, self.url_path)
        
    @staticmethod
    def _modified(soup):
        modified = None
        if soup.date:
            if soup.date.get('type') == 'modified':
                modified = soup.date.text
        return modified
    
    @staticmethod
    def _bytes(soup):
        size = None
        if soup.dataSize:
            try:
                datasize = float(soup.dataSize.text)
                units = soup.dataSize.get('units')
                size = size_in_bytes(datasize, units)
            except:
                logger.exception("dataset size conversion failed")
        return size

    @staticmethod
    def _service_name(soup):
        service_name = None
        try:
            service_tag = soup.servicename
            if service_tag is None:
                service_tag = soup.metadata.servicename
            service_name = service_tag.text
        except:
            logger.exception("dataset has no service_name")
        return service_name

    




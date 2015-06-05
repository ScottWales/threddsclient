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
import urlparse
from .utils import size_in_bytes

import logging
logger = logging.getLogger(__name__)

class Node:
    "Common items to all nodes"
    def __init__(self, soup):
        self.name = soup.get('name')
        self.ID = soup.get('ID')
        self.content_type = None
        self.bytes = None
        self.modified = None

    def __repr__(self):
        return "<Node name: {0.name}, content type: (0.content_type)>".format(self)


class Service(Node):
    "A Thredds service"
    def __init__(self, soup, baseurl):
        Node.__init__(self, soup)
        self.base = soup.get('base')
        self.url = urlparse.urljoin(baseurl, self.base)
        self.serviceType = soup.get('serviceType')
        self.content_type = "application/service"

        self.children = [Service(s, baseurl) for s in
                         soup.find_all('service', recursive=False)]


class Reference(Node):
    "A reference to a different Thredds catalog"
    def __init__(self, soup, baseurl):
        Node.__init__(self, soup)
        self.title = soup.get('xlink:title')
        self.name = self.title
        self.href = soup.get('xlink:href')
        self.url = urlparse.urljoin(baseurl, self.href)
        self.content_type = "application/directory"

    def follow(self):
        from .catalog import readUrl
        return readUrl(self.url)


class Dataset(Node):
    "A reference to a data file"
    def __init__(self, soup):
        Node.__init__(self, soup)
        self.url = soup.get('urlPath')
        self.content_type = "application/netcdf"
        self.modified = self._modified(soup)
        self.bytes = self._bytes(soup)
        
        self.children = [Dataset(d) for d in
                         soup.find_all('dataset', recursive=False)]

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

    




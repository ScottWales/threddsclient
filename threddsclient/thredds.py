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
import pytest
import urlparse

class Node:
    "Common items to all nodes"
    def __init__(self, soup):
        self.name    = soup.get('name')
        self.ID      = soup.get('ID')

class Service(Node):
    "A Thredds service"
    def __init__(self, soup, baseurl):
        Node.__init__(self, soup)
        self.base    = soup.get('base')
        self.url     = urlparse.urljoin(baseurl, self.base)
        self.serviceType = soup.get('serviceType')

        self.children = [Service(s, baseurl) for s in soup.find_all('service', recursive=False)]

class Reference(Node):
    "A reference to a different Thredds catalog"
    def __init__(self, soup, baseurl):
        Node.__init__(self, soup)
        self.href    = soup.get('href')
        self.url     = urlparse.urljoin(baseurl, self.href)

    def follow(self):
        return Catalog.readUrl(self.url)

class Dataset(Node):
    "A reference to a data file"
    def __init__(self, soup):
        Node.__init__(self, soup)
        self.url     = soup.get('urlPath')

        self.children = [Dataset(d) for d in soup.find_all('dataset', recursive=False)]

class TestService:
    def test_unidata_sample_1(self):
        xml="""
        <service name="mcidasServer" serviceType="ADDE" base="http://thredds.ucar.edu/thredds/adde/" />
        """
        soup = BSoup(xml, 'xml')
        s = Service(soup.service, 'http://example.test')
        assert s.name == 'mcidasServer'
        assert s.url  == 'http://thredds.ucar.edu/thredds/adde/' 
        assert s.serviceType == "ADDE"

    def test_unidata_sample_2(self):
        xml="""
        <service name="this" serviceType="DODS" base="dods/" />
        """
        soup = BSoup(xml, 'xml')
        s = Service(soup.service, 'http://example.test')
        assert s.url == 'http://example.test/dods/' 
        
class TestDataset:
    def test_unidata_sample_1(self):
        xml="""
        <dataset name="DC8 flight 1999-11-19" urlPath="SOLVE_DC8_19991119.nc">
          <serviceName>agg</serviceName>
        </dataset>
        """
        soup = BSoup(xml, 'xml')
        d= Dataset(soup.dataset)
        assert d.name == "DC8 flight 1999-11-19"
        assert d.url  == "SOLVE_DC8_19991119.nc"

    def test_unidata_sample_2(self):
        xml="""
        <dataset ID="SOLVE_DC8_19991119" name="DC8 flight 1999-11-19, 1 min merge">
          <metadata xlink:href="http://dataportal.ucar.edu/metadata/tracep_dc8_1min_05"/>
          <access serviceName="disk" urlPath="SOLVE_DC8_19991119.nc"/>
        </dataset>
        """
        soup = BSoup(xml, 'xml')
        Dataset(soup.dataset)

    def test_unidata_sample_3(self):
        xml="""
        <dataset name="Station Data"> 
          <dataset name="Metar data" urlPath="cgi-bin/MetarServer.pl?format=qc" />
          <dataset name="Level 3 Radar data" urlPath="cgi-bin/RadarServer.pl?format=qc" /> 
          <dataset name="Alias to SOLVE dataset" alias="SOLVE_DC8_19991119"/>
        </dataset>
        """
        soup = BSoup(xml, 'xml')
        d = Dataset(soup.dataset)
        assert len(d.children) == 3

class TestReference:
    def test_follow_fqdn(self):
        xml="""
        <catalogRef name="" ID="foo" xlink:href="http://example.test/ref" />
        """
        soup = BSoup(xml, 'xml').catalogRef
        ref  = Reference(soup, 'http://example.test')
        assert ref.url == 'http://example.test/ref'

    def test_follow_rel(self):
        xml="""
        <catalogRef name="" ID="foo" xlink:href="ref" />
        """
        soup = BSoup(xml, 'xml').catalogRef

        ref  = Reference(soup, 'http://example.test/foo')
        assert ref.url == 'http://example.test/ref'

        ref  = Reference(soup, 'http://example.test/foo/')
        assert ref.url == 'http://example.test/foo/ref'

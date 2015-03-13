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

def readUrl(url, **kwargs):
    """
    Create a Catalog from a Thredds catalog link

    :param str url:     URL pointing to a Thredds catalog.xml file
    :param \**kwargs:   Arguments to pass to requests.get() (e.g. for authentication)
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    :raises requests.ConnectionError: if unable to connect to the URL
    """
    req  = requests.get(url, **kwargs)
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
        soup.name # Xml should contain <catalog/> at top level
    except AttributeError:
        raise ValueError("Does not appear to be a Thredds catalog")

    catalog = Catalog()
    catalog.name = soup.get('name')


    # Collect references and datasets
    catalog.services   = [Service(x, baseurl)   for x in soup.find_all('service',    recursive=False)]
    catalog.references = [Reference(x, baseurl) for x in soup.find_all('catalogRef', recursive=False)]
    catalog.datasets   = [Dataset(x)            for x in soup.find_all('dataset',    recursive=False)]

    return catalog

class Catalog:
    "A Thredds catalog entry"
    def __init__(self):
        self.name       = ""
        self.services   = []
        self.references = []
        self.datasets   = []

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

class TestCatalog:
    def test_tpac(self):
        cat = readUrl('http://portal.sf.utas.edu.au/thredds/catalog.xml')

    def test_invalid_url(self):
        with pytest.raises(requests.ConnectionError):
            cat = readUrl('http://example.invalid')

    def test_null(self):
        xml = """
        """
        with pytest.raises(ValueError):
            cat = readXml(xml, 'http://example.test')

    def test_empty(self):
        xml = """
        <catalog></catalog>
        """
        cat = readXml(xml, 'http://example.test')
        assert len(cat.references) == 0
        assert len(cat.datasets)   == 0

    def test_ref(self):
        xml = """
        <catalog><catalogRef name='' ID='foo' /></catalog>
        """
        cat = readXml(xml, 'http://example.test')
        assert len(cat.references) == 1
        assert len(cat.datasets)   == 0

    def test_data(self):
        xml = """
        <catalog><dataset name='' ID='foo' /></catalog>
        """
        cat = readXml(xml, 'http://example.test')
        assert len(cat.references) == 0
        assert len(cat.datasets)   == 1

    def test_unidata_sample(self):
        xml = """
        <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.1" >
          <service name="aggServer" serviceType="DODS"  base="http://acd.ucar.edu/dodsC/" />
          <dataset name="SAGE III Ozone Loss" urlPath="sage.nc">
            <serviceName>aggServer</serviceName>
          </dataset>
        </catalog>
        """
        cat = readXml(xml, 'http://example.test/catalog.xml')
        d   = cat.datasets[0]
        assert d.name == "SAGE III Ozone Loss"

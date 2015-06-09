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

import pytest

from threddsclient import *


def test_tpac():
    cat = read_url('http://portal.sf.utas.edu.au/thredds/catalog.xml')


def test_invalid_url():
    with pytest.raises(requests.ConnectionError):
        cat = read_url('http://example.invalid')


def test_null():
    xml = """
    """
    with pytest.raises(ValueError):
        cat = read_xml(xml, 'http://example.test')


def test_empty():
    xml = """
    <catalog></catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert len(cat.references) == 0
    assert len(cat.datasets) == 0


def test_ref():
    xml = """
    <catalog><catalogRef name='' ID='foo' xlink:title='foo' /></catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert len(cat.references) == 1
    assert len(cat.datasets) == 0


def test_data():
    xml = """
    <catalog><dataset name='' ID='foo' urlPath='' /></catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert len(cat.references) == 0
    assert len(cat.datasets) == 1


def test_unidata_sample():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.1" >
      <service name="aggServer" serviceType="DODS"  base="http://acd.ucar.edu/dodsC/" />
      <dataset name="SAGE III Ozone Loss" urlPath="sage.nc">
        <serviceName>aggServer</serviceName>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    d = cat.datasets[0]
    assert d.name == "SAGE III Ozone Loss"


def test_noaa_catalog():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" name="THREDDS PSD Test Catalog" version="1.0.1">
      <service name="all" serviceType="Compound" base="">
        <service name="odap" serviceType="OPENDAP" base="/psd/thredds/dodsC/" />
        <service name="http" serviceType="HTTPServer" base="/psd/thredds/fileServer/" />
        <service name="wcs" serviceType="WCS" base="/psd/thredds/wcs/" />
        <service name="wms" serviceType="WMS" base="/psd/thredds/wms/" />
      </service>
      <catalogRef name="" xlink:href="/psd/thredds/catalog/Datasets/catalog.xml" xlink:title="Datasets">
        <metadata inherited="true">
          <serviceName>all</serviceName>
          <dataType>GRID</dataType>
        </metadata>
        <property name="DatasetScan" value="true" />
      </catalogRef>
      <catalogRef xlink:href="aggregations.xml" xlink:title="Aggregations" name="" />
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.name == "THREDDS PSD Test Catalog"
    assert cat.services[0].name == 'all'
    assert cat.services[0].service_type == 'Compound'
    assert cat.services[0].url == 'http://example.test/catalog.xml'
    assert cat.services[0].services[0].name == 'odap'
    assert cat.services[0].services[0].service_type == 'OPENDAP'
    assert cat.services[0].services[0].url == 'http://example.test/psd/thredds/dodsC/'
    assert cat.references[0].name == "Datasets"
    assert cat.references[1].name == "Aggregations"

def test_noaa_datasets():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">
      <service name="all" serviceType="Compound" base="">
        <service name="odap" serviceType="OPENDAP" base="/psd/thredds/dodsC/" />
        <service name="http" serviceType="HTTPServer" base="/psd/thredds/fileServer/" />
        <service name="wcs" serviceType="WCS" base="/psd/thredds/wcs/" />
        <service name="wms" serviceType="WMS" base="/psd/thredds/wms/" />
      </service>
      <dataset name="Datasets" ID="Datasets">
        <metadata inherited="true">
          <serviceName>all</serviceName>
          <dataType>GRID</dataType>
        </metadata>
        <catalogRef xlink:href="ncep.reanalysis/catalog.xml" xlink:title="ncep.reanalysis" ID="Datasets/ncep.reanalysis" name="" />
        <catalogRef xlink:href="ncep.reanalysis.dailyavgs/catalog.xml" xlink:title="ncep.reanalysis.dailyavgs" ID="Datasets/ncep.reanalysis.dailyavgs" name="" />
        <catalogRef xlink:href="ncep.reanalysis2/catalog.xml" xlink:title="ncep.reanalysis2" ID="Datasets/ncep.reanalysis2" name="" />
        <catalogRef xlink:href="ncep.reanalysis2.dailyavgs/catalog.xml" xlink:title="ncep.reanalysis2.dailyavgs" ID="Datasets/ncep.reanalysis2.dailyavgs" name="" />
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.services[0].services[1].name == 'http'
    assert cat.services[0].services[1].service_type == 'HTTPServer'
    assert cat.services[0].services[1].url == 'http://example.test/psd/thredds/fileServer/'
    assert cat.datasets[0].name == "Datasets"
    assert cat.datasets[0].content_type == "application/directory"
    assert cat.datasets[0].references[0].name == "ncep.reanalysis"
    assert cat.datasets[0].references[0].url == "http://example.test/ncep.reanalysis/catalog.xml"

def test_noaa_datasets_dailyavgs():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">
      <service name="all" serviceType="Compound" base="">
        <service name="odap" serviceType="OPENDAP" base="/psd/thredds/dodsC/" />
        <service name="http" serviceType="HTTPServer" base="/psd/thredds/fileServer/" />
        <service name="wcs" serviceType="WCS" base="/psd/thredds/wcs/" />
        <service name="wms" serviceType="WMS" base="/psd/thredds/wms/" />
      </service>
      <dataset name="ncep.reanalysis2.dailyavgs" ID="Datasets/ncep.reanalysis2.dailyavgs">
        <metadata inherited="true">
          <serviceName>all</serviceName>
          <dataType>GRID</dataType>
        </metadata>
        <catalogRef xlink:href="gaussian_grid/catalog.xml" xlink:title="gaussian_grid" ID="Datasets/ncep.reanalysis2.dailyavgs/gaussian_grid" name="" />
        <catalogRef xlink:href="pressure/catalog.xml" xlink:title="pressure" ID="Datasets/ncep.reanalysis2.dailyavgs/pressure" name="" />
        <catalogRef xlink:href="surface/catalog.xml" xlink:title="surface" ID="Datasets/ncep.reanalysis2.dailyavgs/surface" name="" />
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.services[0].services[3].name == 'wms'
    assert cat.services[0].services[3].service_type == 'WMS'
    assert cat.services[0].services[3].url == 'http://example.test/psd/thredds/wms/'
    assert cat.datasets[0].name == "ncep.reanalysis2.dailyavgs"
    assert cat.datasets[0].content_type == "application/directory"
    assert cat.datasets[0].references[2].name == "surface"
    assert cat.datasets[0].references[2].url == "http://example.test/surface/catalog.xml"


def test_noaa_datasets_dailyavg_surface():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">
      <service name="all" serviceType="Compound" base="">
        <service name="odap" serviceType="OPENDAP" base="/psd/thredds/dodsC/" />
        <service name="http" serviceType="HTTPServer" base="/psd/thredds/fileServer/" />
        <service name="wcs" serviceType="WCS" base="/psd/thredds/wcs/" />
        <service name="wms" serviceType="WMS" base="/psd/thredds/wms/" />
      </service>
      <dataset name="surface" ID="Datasets/ncep.reanalysis2.dailyavgs/surface">
        <metadata inherited="true">
          <serviceName>all</serviceName>
          <dataType>GRID</dataType>
        </metadata>
        <dataset name="mslp.1980.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc">
          <dataSize units="Mbytes">7.706</dataSize>
          <date type="modified">2011-06-14T00:17:05Z</date>
        </dataset>
        <dataset name="mslp.1981.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1981.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1981.nc">
          <dataSize units="Mbytes">7.685</dataSize>
          <date type="modified">2011-06-14T00:17:16Z</date>
        </dataset>
        <dataset name="mslp.1982.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1982.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1982.nc">
          <dataSize units="Mbytes">7.685</dataSize>
          <date type="modified">2011-06-14T00:17:14Z</date>
        </dataset>
        <dataset name="mslp.1983.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1983.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1983.nc">
          <dataSize units="Mbytes">7.685</dataSize>
          <date type="modified">2011-06-14T00:16:56Z</date>
        </dataset>
        <dataset name="mslp.1984.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1984.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1984.nc">
          <dataSize units="Mbytes">7.706</dataSize>
          <date type="modified">2011-06-14T00:17:19Z</date>
        </dataset>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.datasets[0].name == "surface"
    assert cat.datasets[0].content_type == "application/directory"
    assert cat.datasets[0].datasets[0].name == "mslp.1980.nc"
    assert cat.datasets[0].datasets[0].url == "http://example.test/catalog.xml?dataset=Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc"

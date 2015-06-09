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


def test_noaa_sample():
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
    assert cat.references[0].name == "Datasets"
    assert cat.references[1].name == "Aggregations"

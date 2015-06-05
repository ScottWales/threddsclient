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
import pytest

from threddsclient import *


def test_unidata_sample_1():
    xml = """
    <dataset name="DC8 flight 1999-11-19"
    urlPath="SOLVE_DC8_19991119.nc">
      <serviceName>agg</serviceName>
    </dataset>
    """
    soup = BSoup(xml, 'xml')
    d = Dataset(soup.dataset)
    assert d.name == "DC8 flight 1999-11-19"
    assert d.url == "SOLVE_DC8_19991119.nc"


def test_unidata_sample_2():
    xml = """
    <dataset ID="SOLVE_DC8_19991119" name="DC8 flight 1999-11-19, 1 min merge">
      <metadata xlink:href="http://dataportal.ucar.edu/metadata/tracep_dc8_1min_05"/>
      <access serviceName="disk" urlPath="SOLVE_DC8_19991119.nc"/>
    </dataset>
    """
    soup = BSoup(xml, 'xml')
    Dataset(soup.dataset)


def test_unidata_sample_3():
    xml = """
    <dataset name="Station Data">
      <dataset name="Metar data" urlPath="cgi-bin/MetarServer.pl?format=qc" />
      <dataset name="Level 3 Radar data" urlPath="cgi-bin/RadarServer.pl?format=qc" />
      <dataset name="Alias to SOLVE dataset" alias="SOLVE_DC8_19991119"/>
    </dataset>
    """
    soup = BSoup(xml, 'xml')
    d = Dataset(soup.dataset)
    assert len(d.children) == 3

def test_noaa_sample_1():
    xml = """
    <dataset name="mslp.1979.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc">
      <dataSize units="Mbytes">7.685</dataSize>
      <date type="modified">2011-06-14T00:17:11Z</date>
      <metadata inherited="true">
        <serviceName>all</serviceName>
        <dataType>GRID</dataType>
      </metadata>
    </dataset>
    """
    soup = BSoup(xml, 'xml')
    d = Dataset(soup.dataset)
    assert d.name == "mslp.1979.nc"
    assert d.ID == "Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc"
    assert d.url == "Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc"
    assert d.bytes == 7685000
    assert d.modified == "2011-06-14T00:17:11Z"
    assert d.content_type == "application/netcdf"
    

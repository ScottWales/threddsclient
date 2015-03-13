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
    xml="""
    <service name="mcidasServer" serviceType="ADDE" base="http://thredds.ucar.edu/thredds/adde/" />
    """
    soup = BSoup(xml, 'xml')
    s = Service(soup.service, 'http://example.test')
    assert s.name == 'mcidasServer'
    assert s.url  == 'http://thredds.ucar.edu/thredds/adde/' 
    assert s.serviceType == "ADDE"

def test_unidata_sample_2():
    xml="""
    <service name="this" serviceType="DODS" base="dods/" />
    """
    soup = BSoup(xml, 'xml')
    s = Service(soup.service, 'http://example.test')
    assert s.url == 'http://example.test/dods/' 

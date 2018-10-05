import requests

import pytest

from threddsclient import read_xml, read_url


def test_tpac():
    # cat = read_url('http://portal.sf.utas.edu.au/thredds/catalog.xml')
    pass


def test_invalid_url():
    with pytest.raises(requests.ConnectionError):
        read_url('http://example.invalid')


def test_null():
    xml = """
    """
    with pytest.raises(ValueError):
        read_xml(xml, 'http://example.test')


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


def test_unidata_sample_1():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.1" >
      <service name="mcidasServer" serviceType="ADDE" base="http://thredds.ucar.edu/thredds/adde/" />
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert cat.services[0].name == 'mcidasServer'
    assert cat.services[0].url == 'http://thredds.ucar.edu/thredds/adde/'
    assert cat.services[0].service_type == "ADDE"


def test_unidata_sample_2():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.1" >
      <service name="this" serviceType="DODS" base="dods/" />
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert cat.services[0].url == 'http://example.test/dods/'

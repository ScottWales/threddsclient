import pytest

from threddsclient import *


def test_utas_tpac():
    cat = read_url('http://portal.sf.utas.edu.au/thredds/catalog.xml')
    assert cat.name == 'TPAC Digital Library Data Server Catalog'
    assert cat.url == 'http://portal.sf.utas.edu.au/thredds/catalog.xml'


def test_utas_tpac_html():
    cat = read_url('http://portal.sf.utas.edu.au/thredds/catalog.html')
    assert cat.name == 'TPAC Digital Library Data Server Catalog'
    assert cat.url == 'http://portal.sf.utas.edu.au/thredds/catalog.xml'

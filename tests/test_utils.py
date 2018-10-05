import pytest
from threddsclient import utils


def test_fix_catalog_url():
    assert utils.fix_catalog_url("http://example.org/thredds/catalog.xml") == "http://example.org/thredds/catalog.xml"
    assert utils.fix_catalog_url("http://example.org/thredds/catalog.html") == "http://example.org/thredds/catalog.xml"
    assert utils.fix_catalog_url("http://example.org/thredds/") == "http://example.org/thredds/catalog.xml"
    assert utils.fix_catalog_url("http://example.org/thredds") == "http://example.org/thredds/catalog.xml"

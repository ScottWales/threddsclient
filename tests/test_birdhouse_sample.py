import pytest

from threddsclient import *

def test_birdhouse_sample():
    xml = """
        <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">
          <service name="all" serviceType="Compound" base="">
            <service name="service4" serviceType="HTTPServer" base="/thredds/fileServer/" />
            <service name="odap" serviceType="OPENDAP" base="/thredds/dodsC/" />
            <service name="wcs" serviceType="WCS" base="/thredds/wcs/" />
            <service name="wms" serviceType="WMS" base="/thredds/wms/" />
          </service>
          <dataset name="Test all files in a directory" ID="testDatasetScan">
            <metadata inherited="true">
              <serviceName>all</serviceName>
            </metadata>
            <catalogRef xlink:href="malleefowl/catalog.xml" xlink:title="malleefowl" ID="testDatasetScan/malleefowl" name="" />
            <catalogRef xlink:href="hummingbird/catalog.xml" xlink:title="hummingbird" ID="testDatasetScan/hummingbird" name="" />
            <catalogRef xlink:href="flyingpigeon/catalog.xml" xlink:title="flyingpigeon" ID="testDatasetScan/flyingpigeon" name="" />
            <catalogRef xlink:href="emu/catalog.xml" xlink:title="emu" ID="testDatasetScan/emu" name="" />
          </dataset>
        </catalog>
        """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.name == "Test all files in a directory"
    assert len(cat.datasets) == 1
    assert len(cat.references) == 0
    assert len(cat.flat_datasets()) == 0
    assert len(cat.flat_references()) == 4

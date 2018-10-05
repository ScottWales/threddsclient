import pytest

from threddsclient import read_xml


def test_birdhouse_root():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" name="THREDDS Server Default Catalog" version="1.0.1">  # noqa
      <service name="all" serviceType="Compound" base="">
        <service name="service4" serviceType="HTTPServer" base="/thredds/fileServer/" />
        <service name="odap" serviceType="OPENDAP" base="/thredds/dodsC/" />
        <service name="wcs" serviceType="WCS" base="/thredds/wcs/" />
        <service name="wms" serviceType="WMS" base="/thredds/wms/" />
      </service>
      <catalogRef name="" ID="testDatasetScan" xlink:href="/thredds/catalog/test/catalog.xml" xlink:title="Test all files in a directory">
        <metadata inherited="true">
          <serviceName>all</serviceName>
        </metadata>
        <property name="DatasetScan" value="true" />
      </catalogRef>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test/catalog.xml')
    assert cat.name == "THREDDS Server Default Catalog"
    assert len(cat.datasets) == 0
    assert len(cat.references) == 1
    assert len(cat.flat_datasets()) == 0
    assert len(cat.flat_references()) == 1
    assert len(cat.services) == 1
    assert len(cat.services[0].services) == 4
    assert len(cat.get_services('all')) == 4


def test_birdhouse_top():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">  # noqa
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
    assert cat.flat_references()[0].name == "malleefowl"

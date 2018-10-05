"""
Testing xml sample from noaa catalog: http://www.esrl.noaa.gov/psd/thredds/catalog.xml
"""

import pytest

from threddsclient import read_xml


def test_noaa_catalog():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" name="THREDDS PSD Test Catalog" version="1.0.1">  # noqa
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
    assert len(cat.flat_datasets()) == 0
    assert len(cat.flat_references()) == 2


def test_noaa_datasets():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">  # noqa
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
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">  # noqa
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
    assert cat.datasets[0].ID == "Datasets/ncep.reanalysis2.dailyavgs"
    assert cat.datasets[0].url == "http://example.test/catalog.xml?dataset=Datasets/ncep.reanalysis2.dailyavgs"
    assert cat.datasets[0].content_type == "application/directory"
    assert len(cat.datasets[0].datasets) == 0
    assert len(cat.datasets[0].references) == 3
    assert cat.datasets[0].references[2].name == "surface"
    assert cat.datasets[0].references[2].url == "http://example.test/surface/catalog.xml"
    assert len(cat.flat_datasets()) == 0
    assert len(cat.flat_references()) == 3


def test_noaa_datasets_dailyavg_surface():
    xml = """
    <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0.1">  # noqa
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
    assert cat.services[0].services[2].name == 'wcs'
    assert cat.services[0].services[2].service_type == 'WCS'
    assert cat.services[0].services[2].url == 'http://example.test/psd/thredds/wcs/'
    assert cat.datasets[0].name == "surface"
    assert cat.datasets[0].content_type == "application/directory"
    assert cat.datasets[0].service_name == "all"
    assert cat.datasets[0].data_type == "GRID"
    assert cat.datasets[0].datasets[0].name == "mslp.1980.nc"
    assert cat.datasets[0].datasets[0].ID == "Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc"
    assert cat.datasets[0].datasets[0].url_path == "Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc"
    assert cat.datasets[0].datasets[0].modified == '2011-06-14T00:17:05Z'
    assert cat.datasets[0].datasets[0].bytes == 7706000
    assert cat.datasets[0].datasets[0].data_type == 'GRID'
    assert cat.datasets[0].datasets[0].service_name == 'all'
    assert cat.datasets[0].datasets[0].url == \
        "http://example.test/catalog.xml?dataset=Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc"
    assert cat.datasets[0].datasets[0].download_url() == \
        'http://example.test/psd/thredds/fileServer/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc'
    assert cat.datasets[0].datasets[0].opendap_url() == \
        'http://example.test/psd/thredds/dodsC/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc'
    assert cat.datasets[0].datasets[0].wms_url() == \
        'http://example.test/psd/thredds/wms/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1980.nc'
    assert cat.datasets[0].datasets[0].content_type == 'application/netcdf'
    assert len(cat.download_urls()) == 5
    assert cat.download_urls()[1] == \
        "http://example.test/psd/thredds/fileServer/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1981.nc"
    assert len(cat.opendap_urls()) == 5
    assert cat.opendap_urls()[2] == \
        "http://example.test/psd/thredds/dodsC/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1982.nc"
    assert len(cat.flat_datasets()) == 5
    assert len(cat.flat_references()) == 0

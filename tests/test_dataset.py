import pytest

from threddsclient import read_xml


def test_unidata_sample_1():
    xml = """
    <catalog>
      <dataset name="DC8 flight 1999-11-19" urlPath="SOLVE_DC8_19991119.nc">
        <serviceName>agg</serviceName>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert cat.datasets[0].name == "DC8 flight 1999-11-19"


def test_unidata_sample_2():
    xml = """
    <catalog>
      <dataset ID="SOLVE_DC8_19991119" name="DC8 flight 1999-11-19, 1 min merge">
        <metadata xlink:href="http://dataportal.ucar.edu/metadata/tracep_dc8_1min_05"/>
        <access serviceName="disk" urlPath="SOLVE_DC8_19991119.nc"/>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert cat.datasets[0].name == "DC8 flight 1999-11-19, 1 min merge"


def test_unidata_sample_3():
    xml = """
    <catalog>
      <dataset name="Station Data">
        <dataset name="Metar data" urlPath="cgi-bin/MetarServer.pl?format=qc" />
        <dataset name="Level 3 Radar data" urlPath="cgi-bin/RadarServer.pl?format=qc" />
        <dataset name="Alias to SOLVE dataset" alias="SOLVE_DC8_19991119"/>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    assert len(cat.flat_datasets()) == 2
    # TODO: handle alias dataset


def test_noaa_sample_1():
    xml = """
    <catalog>
      <dataset name="mslp.1979.nc" ID="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc" urlPath="Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc">  # noqa
        <dataSize units="Mbytes">7.685</dataSize>
        <date type="modified">2011-06-14T00:17:11Z</date>
        <metadata inherited="true">
          <serviceName>all</serviceName>
          <dataType>GRID</dataType>
        </metadata>
      </dataset>
    </catalog>
    """
    cat = read_xml(xml, 'http://example.test')
    d = cat.datasets[0]
    assert d.name == "mslp.1979.nc"
    assert d.ID == "Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc"
    assert d.url == "http://example.test?dataset=Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.1979.nc"
    assert d.bytes == 7685000
    assert d.modified == "2011-06-14T00:17:11Z"
    assert d.content_type == "application/netcdf"

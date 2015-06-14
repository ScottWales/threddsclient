# Thredds Client for Python

[![Travis Build](https://travis-ci.org/bird-house/threddsclient.svg?branch=master)](https://travis-ci.org/bird-house/threddsclient)
[![Install with Conda](https://binstar.org/birdhouse/threddsclient/badges/installer/conda.svg)](https://binstar.org/birdhouse/threddsclient)
![License](https://binstar.org/birdhouse/threddsclient/badges/license.svg)]

## Installing Thredds Client

### Anaconda

[![Binstar Build](https://binstar.org/birdhouse/threddsclient/badges/build.svg)](https://binstar.org/birdhouse/threddsclient)
[![Version](https://binstar.org/birdhouse/threddsclient/badges/version.svg)](https://binstar.org/birdhouse/threddsclient)
[![Downloads](https://binstar.org/birdhouse/threddsclient/badges/downloads.svg)](https://binstar.org/birdhouse/threddsclient)

Thredds client is available as Anaconda package. Install it with the following command:

``` bash
$ conda install -c birdhouse threddsclient
```

### From github

Prepare a conda environment with the Python dependencies and activate it:

``` bash
$ conda create python=2.7 lxml beautiful-soup requests -n threddsclient
$ source activate threddsclient
```

Clone the threddslclient github repo and install the Python module:

``` bash
$ git clone https://github.com/bird-house/threddsclient.git
$ cd threddsclient
$ python setup.py develop
```

## Using Thredds Client

### Get download URLs of a catalog

``` python
    import threddsclient
    urls = threddsclient.download_urls('http://example.com/thredds/climate_datasets/catalog.xml')
```

### Get OpenDAP URLs of a catalog

``` python
    import threddsclient
    urls = threddsclient.opendap_urls('http://example.com/thredds/climate_datasets/catalog.xml')
```

### Navigate in catalog and retrieve resources

Start reading a catalog

``` python
    import threddsclient
    cat = threddsclient.read_url('http://example.com/thredds/catalog.xml')
```

Get a list of references to other catalogs & follow them

``` python
    refs = cat.references

    print refs[0].name
    cat2 = refs[0].follow
```

Get a list of datasets in this catalog

```python
    data  = cat.datasets
```

Get flat list of all direct datasets (data files) in the catalog

```python
    datasets = cat.flat_datasets()
    for ds in datasets:
      print ds.name
```

Get flat list of all references in the catalog

```python
    references = cat.flat_references()
    for ref in references:
      print ref.name
```


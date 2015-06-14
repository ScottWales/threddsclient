# Thredds Client for Python

[![Travis Build](https://travis-ci.org/bird-house/threddsclient.svg?branch=master)](https://travis-ci.org/bird-house/threddsclient)
[![Install with Conda](https://binstar.org/birdhouse/threddsclient/badges/installer/conda.svg)](https://binstar.org/birdhouse/threddsclient)
![License](https://binstar.org/birdhouse/threddsclient/badges/license.svg)

## Installing Thredds Client

### Anaconda

[![Binstar Build](https://binstar.org/birdhouse/threddsclient/badges/build.svg)](https://binstar.org/birdhouse/threddsclient)
![Version](https://binstar.org/birdhouse/threddsclient/badges/version.svg)
![Downloads](https://binstar.org/birdhouse/threddsclient/badges/downloads.svg)

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
    urls = threddsclient.download_urls('http://example.com/thredds/catalog.xml')
```

### Get OpenDAP URLs of a catalog

``` python
    import threddsclient
    urls = threddsclient.opendap_urls('http://example.com/thredds/catalog.xml')
```

### Navigate in catalog

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
```

Get flat list of all references in the catalog

```python
    references = cat.flat_references()
```

## Example with NOAA Thredds Catalog

See the IPython Notebook ...


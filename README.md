Thredds Client for Python
=========================
[![Build Status](https://travis-ci.org/bird-house/threddsclient.svg?branch=master)](https://travis-ci.org/bird-house/threddsclient)
[![Install with Conda](https://binstar.org/birdhouse/threddsclient/badges/installer/conda.svg)](https://binstar.org/birdhouse/threddsclient)
[![Binstar Build](https://binstar.org/birdhouse/threddsclient/badges/build.svg)](https://binstar.org/birdhouse/threddsclient)


Start reading a catalogue

```python
    import threddsclient
    cat = threddsclient.read_url('http://example.com/thredds/catalog.xml')
```

Get a list of links to other catalogues & follow them

```python
    links = c.references

    print links[0].name
    cat2 = links[0].follow
```

Get a list of datasets in this catalogue

```python
    data  = cat.datasets
```

Get flat list of all direct datasets (data files) in the catalogue

```python
    datasets = cat.flat_datasets()
```

Get flat list of all references in the catalogue

```python
    datasets = cat.flat_references()
```

Get download URLs of all direct datasets

```python
    urls = cat.download_urls()
    # or use shortcut
    urls = threddsclient.download_urls('http://example.com/thredds/catalog.xml')

Get OpenDAP URLs of all direct datasets

```python
    urls = cat.opendap_urls()
    # or use shortcut
    urls = threddsclient.opendap_urls('http://example.com/thredds/catalog.xml')


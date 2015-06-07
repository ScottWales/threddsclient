Thredds Client for Python
=========================
[![Build Status](https://travis-ci.org/ScottWales/threddsclient.svg?branch=master)](https://travis-ci.org/ScottWales/threddsclient)
[![Coverage Status](https://coveralls.io/repos/ScottWales/threddsclient/badge.svg)](https://coveralls.io/r/ScottWales/threddsclient)

Start reading a catalogue

```python
    import threddsclient
    c = threddsclient.read_url('http://example.com/thredds/catalog.xml')
```

Get a list of links to other catalogues & follow them

```python
    links = c.references

    print links[0].name
    c2 = links[0].follow
```

Get a list of data files in this catalogue

```python
    data  = c.datasets
```

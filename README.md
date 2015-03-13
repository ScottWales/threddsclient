Thredds Client for Python
=========================

Start reading a catalogue

```python
    import threddsclient
    c = threddsclient.readUrl('http://example.com/thredds/catalog.xml')
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

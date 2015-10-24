Thredds Client for Python
=========================

.. image:: https://travis-ci.org/bird-house/threddsclient.svg?branch=master
   :target: https://travis-ci.org/bird-house/threddsclient
   :alt: Travis Build


Installing Thredds Client
-------------------------

Anaconda
~~~~~~~~

|Binstar Build| |Version| |Downloads|

Thredds client is available as Anaconda package. Install it with the
following command:

.. code:: bash

    $ conda install -c birdhouse threddsclient

From github
~~~~~~~~~~~

Prepare a conda environment with the Python dependencies and activate
it:

.. code:: bash

    $ conda create python=2.7 lxml beautiful-soup requests -n threddsclient
    $ source activate threddsclient

Clone the threddslclient github repo and install the Python module:

.. code:: bash

    $ git clone https://github.com/bird-house/threddsclient.git
    $ cd threddsclient
    $ python setup.py develop

Using Thredds Client
--------------------

Read the Thredds tutorial on catalogs: `Thredds Catalog
Primer <http://www.unidata.ucar.edu/software/thredds/current/tds/tutorial/CatalogPrimer.html>`__

Get download URLs of a catalog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

        import threddsclient
        urls = threddsclient.download_urls('http://example.com/thredds/catalog.xml')

Get OpenDAP URLs of a catalog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

        import threddsclient
        urls = threddsclient.opendap_urls('http://example.com/thredds/catalog.xml')

Navigate in catalog
~~~~~~~~~~~~~~~~~~~

Start reading a catalog

.. code:: python

        import threddsclient
        cat = threddsclient.read_url('http://example.com/thredds/catalog.xml')

Get a list of references to other catalogs & follow them

.. code:: python

        refs = cat.references

        print refs[0].name
        cat2 = refs[0].follow()

Get a list of datasets in this catalog

.. code:: python

        data  = cat.datasets

Get flat list of all direct datasets (data files) in the catalog

.. code:: python

        datasets = cat.flat_datasets()

Get flat list of all references in the catalog

.. code:: python

        references = cat.flat_references()

Crawl thredds catalog
~~~~~~~~~~~~~~~~~~~~~

Crawl recursive all direct datasets in catalog following the catalog
references. Stop recusion at a given depth level.

.. code:: python

       import threddsclient
       for ds in threddsclient.crawl('http://example.com/thredds/catalog.xml', depth=2):
           print ds.name
       

Examples with IPython Notebook
------------------------------

-  `NOAA Thredds
   Catalog <http://nbviewer.ipython.org/github/bird-house/threddsclient/blob/master/examples/noaa_example.ipynb>`__

.. |Travis Build| image:: https://travis-ci.org/bird-house/threddsclient.svg?branch=master
   :target: https://travis-ci.org/bird-house/threddsclient
.. |Install with Conda| image:: https://anaconda.org/birdhouse/threddsclient/badges/installer/conda.svg
   :target: https://anaconda.org/birdhouse/threddsclient
.. |License| image:: https://anaconda.org/birdhouse/threddsclient/badges/license.svg
.. |Binstar Build| image:: https://anaconda.org/birdhouse/threddsclient/badges/build.svg
   :target: https://anaconda.org/birdhouse/threddsclient
.. |Version| image:: https://anaconda.org/birdhouse/threddsclient/badges/version.svg
.. |Downloads| image:: https://anaconda.org/birdhouse/threddsclient/badges/downloads.svg

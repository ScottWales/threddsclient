import os
from six.moves.urllib import parse as urlparse


def fix_catalog_url(url):
    """
    Replace .html with .xml extension
    """
    from os.path import splitext, join

    u = urlparse.urlsplit(url)
    name, ext = splitext(u.path)
    if ext == ".html":
        u = urlparse.urlsplit(url.replace(".html", ".xml"))
    elif ext == '':
        u = urlparse.urlsplit(join(url, "catalog.xml"))
    return u.geturl()


def construct_url(url, href):
    u = urlparse.urlsplit(url)
    base_url = u.scheme + "://" + u.netloc
    relative_path = urlparse.urljoin(base_url, os.path.split(u.path)[0])

    if href[0] == "/":
        # Absolute paths
        cat = urlparse.urljoin(base_url, href)
    elif href[0:4] == "http":
        # Full HTTP links
        cat = href
    else:
        # Relative paths.
        cat = relative_path + "/" + href

    return cat


def size_in_bytes(size, unit):
    # Convert to bytes
    if unit == "Kbytes":
        size *= 1000.0
    elif unit == "Mbytes":
        size *= 1e+6
    elif unit == "Gbytes":
        size *= 1e+9
    elif unit == "Tbytes":
        size *= 1e+12
    return int(size)

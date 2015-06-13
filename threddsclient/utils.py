def fix_catalog_url(url):
    """
    Replace .html with .xml extension
    """
    import urlparse
    from os.path import splitext

    u = urlparse.urlsplit(url)
    name, ext = splitext(u.path)
    if ext == ".html":
        u = urlparse.urlsplit(url.replace(".html", ".xml"))
    return u.geturl()


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

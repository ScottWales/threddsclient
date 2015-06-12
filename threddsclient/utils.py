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

# TODO: move this code to a better place

def find_references(soup, catalog):
    from .nodes import CatalogRef
    references = []
    for ref in soup.find_all('catalogRef', recursive=False):
        title = ref.get('xlink:title', '')
        if any([x.match(title) for x in catalog.skip]):
            logger.info("Skipping catalogRef based on 'skips'.  Title: {0}".format(title))
            continue
        else:
            references.append(CatalogRef(ref, catalog))
    return references

def find_datasets(soup, catalog):
    from .nodes import CollectionDataset, DirectDataset
    datasets = []
    for ds in soup.find_all('dataset', recursive=False):    
        name = ds.get("name")
        if any([x.match(name) for x in catalog.skip]):
            logger.info("Skipping dataset based on 'skips'.  Name: {0}".format(name))
            continue
        elif ds.get('urlPath') is None:
            datasets.append( CollectionDataset(ds, catalog) )
        else:
            datasets.append( DirectDataset(ds, catalog) )
    return datasets



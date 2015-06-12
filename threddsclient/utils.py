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
import urlparse
import re

SKIPS = [".*files.*", ".*Individual Files.*", ".*File_Access.*", ".*Forecast Model Run.*", ".*Constant Forecast Offset.*", ".*Constant Forecast Date.*", "\..*"]


def skip_pattern(skip=None):
    # Skip these dataset links, such as a list of files
    # ie. "files/"
    if skip is None:
        skip = SKIPS
    skip = map(lambda x: re.compile(x), skip)
    return skip

def find_references(soup, catalog, skip):
    from .nodes import CatalogRef
    references = []
    for ref in soup.find_all('catalogRef', recursive=False):
        title = ref.get('xlink:title', '')
        if any([x.match(title) for x in skip]):
            logger.info("Skipping catalogRef based on 'skips'.  Title: {0}".format(title))
            continue
        else:
            references.append(CatalogRef(ref, catalog))
    return references

def find_datasets(soup, catalog, skip):
    from .nodes import CollectionDataset, DirectDataset
    datasets = []
    for ds in soup.find_all('dataset', recursive=False):    
        name = ds.get("name")
        if any([x.match(name) for x in skip]):
            logger.info("Skipping dataset based on 'skips'.  Name: {0}".format(name))
            continue
        elif ds.get('urlPath') is None:
            datasets.append( CollectionDataset(ds, catalog, skip) )
        else:
            datasets.append( DirectDataset(ds, catalog) )
    return datasets

def flat_datasets(datasets):
    flat_ds = []
    for ds in datasets:
        if ds.is_collection():
            flat_ds.extend(flat_datasets(ds.datasets))
        else:
            flat_ds.append(ds)
    return flat_ds

def flat_references(datasets):
    flat_refs = []
    for ds in datasets:
        if ds.is_collection():
            flat_refs.extend(ds.references)
            flat_refs.extend(flat_references(ds.datasets))
    return flat_refs

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

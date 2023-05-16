def switch_key(key):
    if key.startswith('#'):
        return key[1:]
    else:
        return key.split("@")[0]

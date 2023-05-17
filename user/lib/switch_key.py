def switch_key(tkey):
    if tkey.startswith('#'):
        key =  tkey[1:]
    else:
        key =  tkey.split("@")[0]
    return key

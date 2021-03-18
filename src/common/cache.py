# #####cache.py 临时cache，后续用Redis替代。
global_cache_dict = {}


def push(key, value):
    global global_cache_dict
    global_cache_dict[key] = value
    return True


def get(key):
    global global_cache_dict
    res = global_cache_dict.get(key)
    return res


def remove(key):
    global global_cache_dict
    global_cache_dict.pop(key,None)
    return True


if __name__ == '__main__':
    global_cache_dict.pop("key",None)

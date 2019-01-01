from yaggal import store

def get_last(params):
    last_list = list(store.query_latest(params))
    if len(last_list) == 0:
        return {}
    return last_list[0]
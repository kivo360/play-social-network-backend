from yaggal import store


if __name__ == "__main__":
    store.delete_many({"type": "jwt"})
    us = store.query({'type': 'jwt'}) 
    print(list(us))
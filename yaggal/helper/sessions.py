import sys
import jwt
import uuid
import time 
from yaggal import store, get_last
from loguru import logger

__SECRET__ = 'qiwlubsoauldbx'

def create_user_key(user_uuid, expiration=3600):

    payload = {
        "uid": user_uuid
    }

    headers = {'kid': str(uuid.uuid4())}
    encoded_jwt =  jwt.encode(payload, __SECRET__, algorithm='HS256', headers=headers).decode("utf-8")



    latest = list(store.query_latest({
        "type": "jwt",
        "encoded_jwt": str(encoded_jwt)
    }))

    # print(latest, file=sys.stderr)
    

    if len(latest) > 0:
        curr = latest[0]
        ctime = time.time()
        exp = curr["expiration"]
        creation_time = curr["timestamp"]
        if ((creation_time+exp) < time.time()):
            logger.debug("Over the general time")
            store.store({
                "type": "jwt",
                "encoded_jwt": str(encoded_jwt),
                "timestamp": float(int(time.time())),
                "expiration": expiration
            })
        else:
            print("", file=sys.stderr)
    else:
        store.store({
                "type": "jwt",
                "encoded_jwt": str(encoded_jwt),
                "timestamp": float(int(time.time())),
                "expiration": expiration
            })

    return encoded_jwt


def refresh_token(encoded_jwt, expiration=3600):

    current = get_last({
        "type": "jwt",
        "encoded_jwt": str(encoded_jwt)
    })

    # print(encoded_jwt, file=sys.stderr)
    # print(latest, file=sys.stderr)
    # print(jwt_all, file=sys.stderr)

    if current == {}:
        return {}

    # encoded_jwt = current['encoded_jwt']
    # headers = {'kid': str(uuid.uuid4())}
    user_id = jwt.decode(encoded_jwt, __SECRET__, algorithm='HS256') # We're using this as the new payload

    headers = {'kid': str(uuid.uuid4())}
    encoded_jwt =  jwt.encode(user_id, __SECRET__, algorithm='HS256', headers=headers).decode("utf-8")
    store.store({
                "type": "jwt",
                "encoded_jwt": str(encoded_jwt),
                "timestamp": float(int(time.time())),
                "expiration": expiration
            })
    # latest_users = list()

    return encoded_jwt

def get_user_by_jwt(encoded_jwt):
    
    latest = get_last({
        "type": "jwt",
        "encoded_jwt": str(encoded_jwt)
    })
    # print(encoded_jwt, file=sys.stderr)
    # print(latest, file=sys.stderr)
    # print(jwt_all, file=sys.stderr)

    if latest == {}:
        return {}
    
    current = latest
    timestamp = current['timestamp']
    expire = current['expiration']
    expiration_time = timestamp + expire
    current_time = time.time()

    if expiration_time < current_time:
        return {}
    
    encoded_jwt = current['encoded_jwt']
    
    user_id = jwt.decode(encoded_jwt, __SECRET__, algorithm='HS256')

    latest_users = get_last({"type": "user", "sid": user_id["uid"]})
    return latest_users
    
def get_user_without_check(encoded_jwt):
    """
        This is used to check to see if the user exist and refresh token. 

        return user
    """
    latest = get_last({
        "type": "jwt",
        "encoded_jwt": str(encoded_jwt)
    })
    # print(encoded_jwt, file=sys.stderr)
    # print(latest, file=sys.stderr)
    # print(jwt_all, file=sys.stderr)

    if latest == {}:
        return {}
    
    # current = latest
    # timestamp = current['timestamp']
    # expire = current['expiration']
    # expiration_time = timestamp + expire
    # current_time = time.time()

    # if expiration_time < current_time:
    #     return {}
    # store.store({
    #             "type": "jwt",
    #             "encoded_jwt": str(encoded_jwt),
    #             "timestamp": float(int(time.time())),
    #             "expiration": expiration
    #         })
    # encoded_jwt = current['encoded_jwt']
    user_id = jwt.decode(encoded_jwt, __SECRET__, algorithm='HS256')

    latest_users = get_last({"type": "user", "sid": user_id["uid"]})
    return latest_users
    
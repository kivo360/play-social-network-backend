import sys
import os 



from functools import wraps
from sanic.response import json
from yaggal.helper.sessions import get_user_by_jwt


def check_request_for_authorization(request):
    head = request.headers
    authorization = head.get("Authorization", None)

    if authorization is None:
        return False
    
    
    splits = authorization.split(" ")
    # print(splits, file=sys.stderr)
    if len(splits) != 2:
        return False

    if splits[0] != "Bearer":
        return False

    # Check for authorization online
    if splits[1] == "":
        return False

    user = get_user_by_jwt(splits[1])
    # print()
    # Check to see the authorization is available
    _is_empty = user == {}
    if _is_empty:
        return False

    return True

def inject_user(request):
    head = request.headers
    authorization = head.get("Authorization", None)

    if authorization is None:
        return False
    
    
    splits = authorization.split(" ")
    # print(splits, file=sys.stderr)
    if len(splits) != 2:
        return False, {}

    if splits[0] != "Bearer":
        return False, {}

    # Check for authorization online
    if splits[1] == "":
        return False, {}

    user = get_user_by_jwt(splits[1])
    # print()
    # Check to see the authorization is available
    _is_empty = user == {}
    if _is_empty:
        return False, {}

    return True, user

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized. 
                return json({'msg': 'Not authorized'}, 403)
        return decorated_function
    return decorator

def inject():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = inject_user(request)

            if is_authorized[0]:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, is_authorized[1], *args, **kwargs)
                return response
            else:
                # the user is not authorized. 
                return json({'msg': 'Not authorized'}, 403)
        return decorated_function
    return decorator
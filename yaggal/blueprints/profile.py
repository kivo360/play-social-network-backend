import sys
import time
from sanic import Blueprint, Sanic
from sanic.response import file, json
from yaggal.wrappers.auth import authorized, inject
from yaggal.helper.formatting import general_response
from yaggal import get_last, store

# app = Sanic(__name__)
profile = Blueprint('profile', url_prefix='/profile')

@profile.route("/view", methods=["POST"])
async def pview(request):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}, "JSON Not Found"), status=400)

    _id = r.get("id", None)

    if _id is None:
        return json(general_response("User Id is missing. Please enter it", {}, "User Id Missing"), status=400)
    
    # Find the latest user with the given user id. If nothing is found, return that nothing was found.
    user_list = list(store.query({"type": "user", "sid": _id}))
    if len(user_list) == 0:
        return json(general_response("No user found with that id", {}, "User not found"), status=404)

    # Check to see if we have any account data added in yet.
    account_info = list(store.query({"type": "account", "uid": _id}))
    account_dict = {"type": "account", "uid": _id, "description": "", "pubkey":"...............", "timestamp": time.time()}
    if len(account_info) == 0:
        store.store(account_dict)
        # return json(general_response("No account information found", {}, "Account Not Found"), status=404) 

    # TODO: Check for every user's post as well
    
    query_object = {
        "type": "post",
        "author": _id
    }

    user_posts = list(store.query_latest(query_object))

    return json({"msg": "User was found. Getting the account data too.", "data": user_list[0], "account": account_dict, "posts": user_posts})




@profile.route("/edit", methods=["POST"])
@authorized()
@inject()
async def edit(request, user):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    

    # Figure out what to change based on what we recieve 
    # print(user, file=sys.stderr)
    return json({"msg": "Here we get the authorization code to determine what the user should do."})


@profile.route("/follow", methods=["POST"])
@authorized()
@inject()
async def follow(request, user):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    return json({"msg": "Here we get the authorization code to determine what the user should do."})
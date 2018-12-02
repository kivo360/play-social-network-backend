import sys

from sanic import Blueprint, Sanic
from sanic.response import file, json
from yaggal.wrappers.auth import authorized, inject
from yaggal.helper.formatting import general_response
# app = Sanic(__name__)
profile = Blueprint('profile', url_prefix='/profile')

@profile.route("/view", methods=["POST"])
async def pview(request):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    return json({"msg": "We get the session id to see what the user has done"})




@profile.route("/edit", methods=["POST"])
@authorized()
@inject()
async def edit(request, user):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    
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
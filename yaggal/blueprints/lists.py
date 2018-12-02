import sys

from sanic import Blueprint, Sanic
from sanic.response import file, json

from yaggal import store, get_last
from yaggal.wrappers.auth import authorized, inject
from yaggal.helper.formatting import general_response
# app = Sanic(__name__)
lists = Blueprint('lists', url_prefix='/lists')

@lists.route("/get", methods=["POST"])
async def view(request):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)

    all_posts = list(store.query_latest({"type": "post"}))

    return json({"msg": "Return a list of post", "data": all_posts})


@lists.route("/search", methods=["POST"])
async def search(request):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)

    return json({"msg": "We get the session id to see what the user has done"})


# @profile.route("/publish", methods=["POST"])
# @authorized()
# @inject()
# async def publish(request, user):
#     r = request.json

#     if r is None:
#         return json(general_response("Json not sent in. Please enter it.", {}), status=400)
#     # make sure post text exist
#     # Get the post-text
#     # get the get the post title
#     # create post id
#     # Store post with user-id as reference
#     # Explain to use that the post was created
#     # print(user, file=sys.stderr)
#     return json({"msg": "Here we get the authorization code to determine what the user should do."})

# @profile.route("/edit", methods=["POST"])
# @authorized()
# @inject()
# async def edit(request, user):
#     r = request.json

#     if r is None:
#         return json(general_response("Json not sent in. Please enter it.", {}), status=400)
#     # print(user, file=sys.stderr)
#     return json({"msg": "Here we get the authorization code to determine what the user should do."})

# @profile.route("/editable", methods=["POST"])
# @authorized()
# @inject()
# async def editable(request, user):
#     r = request.json

#     if r is None:
#         return json(general_response("Json not sent in. Please enter it.", {}), status=400)
#     # Get the post id
#     # 
#     # print(user, file=sys.stderr)
#     return json({"msg": "Here we get the authorization code to determine what the user should do."})
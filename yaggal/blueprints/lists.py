import sys

from sanic import Blueprint, Sanic
from sanic.response import file, json

from yaggal import store, get_last
from yaggal.wrappers.auth import authorized, inject
from yaggal.helper.formatting import general_response
from loguru import logger
# from sanic.log import logger
logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")
# app = Sanic(__name__)
lists = Blueprint('lists', url_prefix='/lists')

@lists.route("/get", methods=["POST"])
async def view(request):
    r = request.json
    logger.debug("Getting a list of posts")

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}, title="No JSON"), status=400)

    category = r.get("category")
    page = r.get("page")

    logger.info("{} {}".format(category, page))
    if category is None:
        return json(general_response("Page category required", {}, title="No category given"), status=400)

    if (page is None and category != "home"):
        return json(general_response("No page number given", {}, title="No Page Number"), status=400)



    logger.log("SNAKY", "Category: {} Page: {}".format(category, page))
    # If the category is home, we get all posts. Some information wont be had
    # if category == "home":
    #   all_posts = list(store.query_latest({"type": "post"})) # Put a page limit of 10
    #   Get stats by post (need to get the stats of each post (votes, author information, etc))
    # else:
    #   post_by_category = list(store.query_latest({"type": "post", "tag": category}, pagination=True, page_num=page, page_size=10))
    #   Get stats by post (iterate through each)
    # Return the information here
    all_posts = list(store.query_latest({"type": "post"}))
    

    return json({"msg": "Return a list of post", "data": all_posts})

@lists.route("/get/trending", methods=["POST"])
async def view(request):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}, title="No JSON"), status=400)

    category = r.get("category")
    page = r.get("page")

    # We'll have a background process getting the trending
    if page is None:
        return json(general_response("No page number given", {}, title="No Page Number"), status=400)

    if category is None:
        return json(general_response("Page category required", {}, title="No category given"), status=400)

    # If the category is home, we get all posts. Some information wont be had
    # if category == "home":
    #   all_posts = list(store.query_latest({"type": "post"})) # Put a page limit of 10
    #   Get stats by post (need to get the stats of each post (votes, author information, etc))
    # else:
    #   post_by_category = list(store.query_latest({"type": "post", "tag": category}, pagination=True, page_num=page, page_size=10))
    #   Get stats by post (iterate through each)
    # Return the information here
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
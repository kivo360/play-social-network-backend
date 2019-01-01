import os
import sys
import time
import uuid

from sanic import Blueprint, Sanic
from sanic.response import file, json

from yaggal import get_last, store
from yaggal.helper.formatting import general_response
from yaggal.wrappers.auth import authorized, inject

# app = Sanic(__name__)
posts = Blueprint('post', url_prefix='/post')

@posts.route("/view", methods=["POST"])
async def view(request):
    # Get post-id
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    print(r)
    post_id = r.get("postid", None)

    if post_id is None:
        return json(general_response("No post-id available", {}, title="No Post Id"), status=400)
    
    last = get_last({"type": "post", "pid": post_id})

    if last == {}:
        return json(general_response("The post you're looking for doesn't exist", {}, title="Post Doesn't Exist"), status=400)
    

    # Dont forget to get the vote information(if it exist), and the comments
    comments = list(store.query_latest({"type": "comment", "pid": post_id}))
    votes = list(store.query_latest({"type": "vote", "pid": post_id}))
    main = {
        "post": last,
        "comments": comments,
        "votes": votes
    }
    return json(general_response("Post Successfully Found", main), status=200)


@posts.route("/publish", methods=["POST"])
@authorized()
@inject()
async def publish(request, user):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    
    title = r.get("title", None)
    main = r.get("main", None)
    tags = r.get("tags", None)
    txt = r.get("txt", None)
    img = r.get("img", None)

    if title is None:
        return json(general_response("Post title not given. Please enter it.", {}, title="Missing Title"), status=400)
    
    if main is None:
        return json(general_response("Main tag not given. Please enter.", {}, title="Missing Main Tag"), status=400)
    
    if tags is None:
        return json(general_response("Post tags not entered.", {}, title="Missing Tags"), status=400)

    if txt is None:
        return json(general_response("Post text not given. Please enter.", {}, title="Incorrect Tab Number"), status=400)

    if img is None:
        return json(general_response("Image not found. Please send in an image.", {}, title="Image not found"), status=400)

    if not isinstance(main, str):
        return json(general_response("Make sure the main tag is a string. It can't be a list or anything else.", {}, title="Incorrect Tab Number"), status=400)

    if not isinstance(txt, str):
        return json(general_response("Make sure the main tag is a string. It can't be a list or anything else.", {}, title="Incorrect Tab Number"), status=400)
    
    if not isinstance(tags, list):
        return json(general_response("Make sure tags is a list.", {}, title="Incorrect Tab Type"), status=400)
    
    if len(tags) < 3 or len(tags) > 10:
        return json(general_response("Incorrect number of tags. Between 3 and 10 tags.", {}, title="Incorrect Tab Number"), status=400)
    
    
    # If this is all good, save the post inside of the database
    post_id = str(uuid.uuid4())
    save_obj = {
        "pid": post_id,
        "type": "post",
        "author": user['sid'],
        "title": title,
        "mtag": main,
        "tags": tags,
        "txt": txt,
        "image": img,
        "timestamp": float(time.time())
    }
    
    try:
        store.store(save_obj)
    except Exception:
        return json(general_response("We had a problem on our end. Sorry :(", {}, title="My Bad"), status=500)
    
    return json(general_response("Post Successfully Published", {"post_id": post_id}, title="Publish Successful"))

@posts.route("/edit", methods=["POST"])
@authorized()
@inject()
async def edit(request, user):
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    

    # print(user, file=sys.stderr)
    return json({"msg": "Here we get the authorization code to determine what the user should do."})

@posts.route("/editable", methods=["POST"])
@authorized()
@inject()
async def editable(request, user):
    """ Use to get editable version of a given post. Make sure the current user owns the post"""
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    # Get the post id
    # 
    # print(user, file=sys.stderr)
    return json({"msg": "Here we get the authorization code to determine what the user should do."})


@posts.route("/vote", methods=["POST"])
@authorized()
@inject()
async def vote(request, user):
    """ Use to vote for post """
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    

    post_id = r.get("post-id", None)

    if post_id is None:
        return json(general_response("No post-id available", {}), status=400)

    last = get_last({"type": "post", "pid": post_id})

    if last == {}:
        return json(general_response("Post doesn't exist", {}), status=400)
    voter_id = user['sid']

    last_vote = get_last({"type": "vote", "pid": post_id, "voter": voter_id})

    if last_vote != {}:
        return json(general_response("Already voted. Can't do again", {}), status=400)
    
    # TODO: Add extra voter info
    vote_obj = {
        "type": "vote",
        "pid": post_id,
        "voter": voter_id,
        "timestamp": float(int(time.time()))
    }

    try:
        store.store(vote_obj)
    except Exception:
        return json(general_response("We had a problem on our end. Sorry :(", {}, title="Our Bad"), status=500)
    
    # Get the post id
    # Make sure the post exist
    # The person that votes shouldn't be the person that votes
    # Put a hard limit here
    # get the amount you're voting for
    # Check if the user has enough to vote inside of their account
    # If they do, send command to send money to author
        # Get author-id by post-id
        # Send transaction between the two users
    
    # If not, say to the user they're useless and can't live anymore
    # 
    return json({"msg": "Vote successful"})

@posts.route("/comment", methods=["POST"])
@authorized()
@inject()
async def comment(request, user):
    """ Make the current user comment on a post """
    r = request.json

    if r is None:
        return json(general_response("Json not sent in. Please enter it.", {}), status=400)
    

    post_id = r.get("post-id", None)
    txt = r.get("txt", None)

    if post_id is None:
        return json(general_response("No post-id available", {}), status=400)
    
    if txt is None:
        return json(general_response("Comment text not given. Please enter.", {}), status=400)

    last = get_last({"type": "post", "pid": post_id})

    if last == {}:
        return json(general_response("Post doesn't exist", {}), status=400)

    if not isinstance(txt, str):
        return json(general_response("Make sure the text entered is a string.", {}), status=400)
    
    comment_author_id = user['sid']
    

    save_obj = {
        "type": "comment", 
        "pid": post_id,
        "author": comment_author_id,
        "text": txt, 
        "timestamp": float(int(time.time()))
    }

    try:
        store.store(save_obj)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return json(general_response("We had a problem on our end. Sorry :(", {}), status=500)

    
    
    # Get the post id
    # Make sure the post exist
    # if the person commenting is the author, don't charge, just save and that's it
    # get the amount you're commenting for
    
    # Check if the user has enough to vote inside of their account
    # If they do, send command to send money to author
        # Get author-id by post-id
        # Send transaction between the two users
    
    # If not, say to the user they're useless and can't live anymore
    # 
    return json({"msg": "Comment successfully added."})

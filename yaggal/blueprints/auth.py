import sys
import os
import time
import uuid

from sanic import Blueprint, Sanic
from sanic.response import file, json
from validate_email import validate_email
from passlib.hash import pbkdf2_sha256
from yaggal.helper.sessions import create_user_key, refresh_token

from yaggal import store
from yaggal.helper.validation import validate_password, validate_pin
from yaggal.helper.formatting import general_response
from yaggal.wrappers.auth import authorized, inject, check

auth = Blueprint('auth', url_prefix='/auth')

@auth.route("/login", methods=["POST"])
async def login(request):
    
    r = request.json
    if r is None:
        return json({"msg": "Please enter a json request"}, status=400)

    username  = r.get("username", None)
    password = r.get("password", None)
    email = None
    if username is None or password is None:
        return json({
            "msg": "please enter your username or password",
            "title": "Missing Information"
        }, status=400)

    is_valid_email = validate_email(username)

    if is_valid_email:
        email = username
    
    
    db_email = None
    is_valid = False
    doc_found = False
    # Check for both username and email
    if email is not None:
        db_email = list(store.query({"email": email, "type": "user"}))
    
    if db_email is not None:
        if len(db_email) > 0:
            doc_found = True
            current_doc = db_email[0]
            is_valid = pbkdf2_sha256.verify(password, current_doc["password"])
    
    if is_valid == False:
        db_username = list(store.query({"username": username, "type": "user"}))
        if len(db_username) > 0:
            doc_found = True
            current_doc = db_username[0]
            is_valid = pbkdf2_sha256.verify(password, current_doc["password"])
    
    # print(current_doc, file=sys.stderr)
    # Determine if its valid
    if doc_found == False or is_valid==False:
        return json({
            "msg": "The username or password you entered was not correct",
            "title": "Missing Information"
        }, status=400)
    
    else:
        _id = current_doc['sid']
        _jwt = create_user_key(_id)

        front_dict = {
            "sid": current_doc['sid'],
            "username": current_doc['username'],
            "email": current_doc['email']
        }

        # Set a session id here
        return json({"msg": "Successful", "token": _jwt, "user": front_dict})
    
    
    # Would check for username or password here
    return json({"msg": "Default baby"})


@auth.route("/register", methods=["POST"])
async def register(request):
    r = request.json
    if r is None:
        return json({"msg": "Please enter a json request", "title": "No Json"}, status=400)

    username  = r.get("username", None)
    email = r.get("email", None)
    password = r.get("password", None)
    confirm = r.get("confirm", None)
    pin = r.get("pin", None)


    no_username = username is None
    no_password = password is None
    no_confirm = confirm is None
    no_pin = pin is None
    no_email = email is None

    if no_username:
        return json({
            "msg": "No Username. Please enter a username",
            "title": "No Username"
        }, status=400)
    
    if no_password:
        return json({
            "msg": "No password. Please enter one",
            "title": "No password"
        }, status=400)
    
    if no_confirm:
        return json({
            "msg": "No confirmation password. Please enter one",
            "title": "No confirmation"
        }, status=400)

    if no_pin:
        return json({
            "msg": "No pin. Please enter one",
            "title": "No pin"
        }, status=400)
    
    if no_email:
        return json({
            "msg": "No email. Please enter one",
            "title": "No email"
        }, status=400)

    db_email = list(store.query({"email": email, "type": "user"}))
    db_username = list(store.query({"username": username, "type": "user"}))

    
    # print(db_email, file=sys.stderr)
    # print(db_username, file=sys.stderr)

    if len(db_email) > 0:
        return json({"msg": "That email is already taken", "title": "Email Taken"}, status=400)

    if len(db_username) > 0:
        return json({"msg": "That username is already taken", "title": "Username Taken"}, status=400)

    if confirm != password:
        return json({"msg": "The confirmation and password are not the same", "title": "Invalid Confirmation"}, status=400)

    is_valid_email = validate_email(email)

    if not is_valid_email:
        return json({"msg": "The email you entered is not valid", "title": "Invalid Email"}, status=400)

    
    
    is_valid_password =  validate_password(password)
    if is_valid_password[1] != 200:
        return json({"msg": is_valid_password[0]}, status=is_valid_password[1])
    
    is_valid_pin = validate_pin(pin)
    if is_valid_pin[1] != 200:
        return json({"msg": is_valid_pin[0]}, status=is_valid_pin[1])

    savable = pbkdf2_sha256.hash(password)


    # 

    _sid = str(uuid.uuid4())
    save_dict = {
        "type": "user",
        "sid": _sid, # Will store this inside of the JWT to ensure the user can post and
        "timestamp": time.time(),
        "username": username,
        "password": savable,
        "email": email,
        "pin": pin
    }
    try:
        store.store(save_dict)
    except Exception:
        return json({"msg": "There was a problem on our end. Sorry!!!"}, status=500)
    
    _jwt = create_user_key(_sid)
    front_dict = {
        "sid": _sid,
        "username": username,
        "email": email
    }
    return json({"msg": "Success", "token": _jwt, "user": front_dict})


@auth.route("/refresh", methods=["POST"])
@check()
async def refresh(request, encoded):
    new_token = refresh_token(encoded)
    return json({"msg": "Refresh Successful", "token": new_token})
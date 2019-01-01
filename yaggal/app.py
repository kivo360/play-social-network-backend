import uuid
import aiofiles
import boto3
from sanic import Sanic
from sanic import response as res
from sanic.response import json
from sanic_cors import CORS, cross_origin

from yaggal.blueprints.auth import auth
from yaggal.blueprints.lists import lists
from yaggal.blueprints.posts import posts
from yaggal.blueprints.profile import profile
from yaggal.blueprints.wallet import wallet

from loguru import logger
from sanic.log import LOGGING_CONFIG_DEFAULTS

# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

# ddd = LOGGING_CONFIG_DEFAULTS
# ddd['disable_existing_loggers'] = True
# ddd['loggers']['sanic.access']['propagate'] = False
# logger.info(ddd)
app = Sanic(__name__, log_config=None)
CORS(app, automatic_options=True)



app.blueprint(auth)
app.blueprint(profile)
app.blueprint(posts)
app.blueprint(lists)
app.blueprint(wallet)

ACCEPTED_FILES = ["image/jpeg", "image/png"]


# TODO: Work on this last. Make sure all of the calls work first.
@app.route("/image", methods=["POST"])
async def search(request):
    main_file = request.files.get('file', None)
    # print(main_file.type)
    if main_file is None:
        return json({"msg": "You didn't install the right file", "title": "File not found"}, status=400)
    
    if main_file.type not in ACCEPTED_FILES:
        return json({"msg": "Incorrect file type", "title": "Incorrect File Type"}, status=400)
    

    logger.debug(main_file.type)
    # Upload to S3
    # file_name = str(uuid.uuid1())

    # if main_file.type == "image/jpeg":
    #     file_name+=".jpg"
    # if main_file.type == "image/png":
    #     file_name+=".png"

    # async with aiofiles.open('/tmp/{}'.format(file_name), 'wb') as f:
    #     await f.write(main_file.body)
        # AKIAJCI6AZQMLIUEXFEA
        # Ab1UzRC1NSsF8ZpW9Ja22gZogJeLN/DLC+oPFkwi
        
    # print(main_file.name)
    # print(main_file.type)
    return json({"msg": "Success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False, auto_reload=True, access_log=False)

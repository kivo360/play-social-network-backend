from sanic import Sanic
from sanic import response as res 
from yaggal.blueprints.auth import auth
from yaggal.blueprints.profile import profile
from yaggal.blueprints.posts import posts
from yaggal.blueprints.lists import lists


app = Sanic(__name__)
# Session(app)



app.blueprint(auth)
app.blueprint(profile)
app.blueprint(posts)
app.blueprint(lists)

app.run(host='0.0.0.0', port=8000, debug=True)


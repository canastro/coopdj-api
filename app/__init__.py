# TODO: REFACTOR TO THIS: https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_restful import Api
from app.resources.playlist import Playlist
from app.resources.music import Music
from app.models import db

# https://github.com/MongoEngine/flask-mongoengine/issues/77

#Create our API
app = Flask(__name__)

# Load config.
app.config.from_pyfile('config.cfg', silent=True)

api = Api(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(Playlist, '/playlist')
api.add_resource(Music, '/musics/<int:music_id>')

# Add CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Setup the database.
def init(**config_overrides):

    # apply overrides
    app.config.update(config_overrides)

    db.init_app(app)

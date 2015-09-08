# TODO: REFACTOR TO THIS: https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
import datetime
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flask.ext.mongoengine import MongoEngine
from flask_restful import Api
from app.resources.playlist import Playlist
from app.resources.music import Music
from app.models import db
from app import constants as CONSTANTS

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


# After request, add CORS and log requests
def getResponseLen(response):
    try:
        return len(response.data)
    except:
        return '-'

def getRequestURL(request):
    url = '\"' + request.method
    url += ' /' + request.url.split(request.url_root)[1]
    url += '\"'
    return url

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    app.logger.info('\t'.join([
            request.remote_addr,                                            # client ip
            '-',                                                            # RFC 1413 identity of the client.
            '-',                                                            # user id
            datetime.datetime.today().strftime('[%d/%b/%Y %H:%M:%S]'),      # date time
            getRequestURL(request),
            response.status.split(' ')[0],
            getResponseLen(response.data)
        ]))

    return response

# Setup the database.
def init(**config_overrides):

    print "init------"

    handler = RotatingFileHandler(
        CONSTANTS.LOG_FILENAME,
        maxBytes=1024 * 1024 * 100,
        backupCount=20
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # apply overrides
    app.config.update(config_overrides)

    db.init_app(app)

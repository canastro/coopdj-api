import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_restful import Api
from coopdj_api.resources.musics import Musics
from coopdj_api.resources.music import Music

#Create our API
app = Flask(__name__)
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    MONGODB_SETTINGS={'DB': "coopdj"},
    DEBUG=True,
    SECRET_KEY='secret'
))

# Add CORS
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

from coopdj_api.models import db
db.init_app(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(Musics, '/musics')
api.add_resource(Music, '/musics/<int:music_id>')

if __name__ == '__main__':
    app.run()

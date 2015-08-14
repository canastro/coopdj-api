# TODO: REFACTOR TO THIS: https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_restful import Api
from app.resources.musics import Musics
from app.resources.music import Music
from app.models import db


def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config.
    app.config.from_pyfile('config.cfg', silent=True)
    # apply overrides
    app.config.update(config_overrides)

    # Setup the database.
    db.init_app(app)

    return app


#Create our API
app = create_app()
api = Api(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(Musics, '/musics')
api.add_resource(Music, '/musics/<int:music_id>')

# app = Flask(__name__)
#
#
# # Load default config and override config from an environment variable
# app.config.update(dict(
#     MONGODB_SETTINGS={'DB': "coopdj"},
#     DEBUG=True,
#     SECRET_KEY='secret'
# ))
#
# db.init_app(app)

# Add CORS
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response




if __name__ == '__main__':
    app.run()

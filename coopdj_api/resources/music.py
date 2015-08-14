import datetime
import bson
import requests
from flask import Flask, Response, json
from flask.ext.mongoengine import MongoEngine
from flask_restful import reqparse, abort, Api, Resource, inputs

from coopdj_api.models import MusicModel

def buildResponse(data, status):
    return Response(json.dumps(data), status=status, mimetype='application/json')

# https://flask-restful.readthedocs.org/en/0.3.4/quickstart.html#full-example
# Music
# shows a single music and lets you delete a music
class Music(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Music, self).__init__()

    def get(self, music_id):

        # attempt to retrieve music by music_id
        try:
            music = MusicModel.objects.get(pk=music_id)
        except MusicModel.DoesNotExist:
            return buildResponse('', 404)

        return buildResponse(music, 200)

    def delete(self, music_id):
        return '', 204

    def put(self, music_id):

        self.parser.add_argument('action', help='Action is required', location='args')
        args = self.parser.parse_args()

        # get required action
        action = args['action'].upper()

        # attempt to retrieve music by music_id
        try:
            music = MusicModel.objects.get(pk=music_id)
        except MusicModel.DoesNotExist:
            return buildResponse('', 404)

        # increment music votes
        def voteUp():
            music.votes += 1

        # decrement music votes
        def voteDown():
            music.votes -= 1

        # set music as played
        def play():
            music.has_played = True

        # switch
        options = {
            'VOTE_UP': voteUp,
            'VOTE_DOWN': voteDown,
            'PLAY': play
        }

        # if actions is not present in options object, then request was mal-formed
        if not action in options:
            return buildResponse('', 400)

        # execute action and save music
        options[action]()

        music.save()

        return buildResponse('', 200)

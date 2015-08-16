import datetime
import bson
import requests
from flask import Flask, Response, json
from flask.ext.mongoengine import MongoEngine
from flask_restful import reqparse, abort, Api, Resource, inputs

from app import constants as CONSTANTS
from app.models import MusicModel

def buildResponse(data, status):
    return Response(json.dumps(data), status=status, mimetype='application/json')

def buildYoutubeQueryURL(videoId):
    url = CONSTANTS.YOUTUBE_API_BASE + CONSTANTS.YOUTUBE_API_VIDEO_DETAILS
    url = url.replace('#VIDEO_ID#', videoId)

    return url

# Playlist
# shows a list of all todos, and lets you POST to add new tasks
class Playlist(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Playlist, self).__init__()

    def get(self):

        self.parser.add_argument(
            'action',
            help='Action is required',
            location='args',
            required=True
        )
        args = self.parser.parse_args()

        action = args['action'].upper()

        # get all musics
        def getAll():
            return buildResponse(MusicModel.objects.all().order_by('-votes' ,'_id'), 200)

        def getNext():
            music = MusicModel.objects(has_played=False).order_by('-votes','_id').first()
            return buildResponse(music, 200)

        options = {
            'ALL': getAll,
            'NEXT': getNext
        }

        # if actions is not present in options object, then request was mal-formed
        if not action in options:
            return buildResponse('', 400)

        # execute action and save music
        return options[action]()

    def post(self):

        self.parser.add_argument(
            'url',
            type=inputs.regex(CONSTANTS.YOUTUBE_URL_REGEX),
            help='Url is required',
            required=True
        )

        self.parser.add_argument(
            'type',
            help='Type is required',
            required=True
        )

        args = self.parser.parse_args()

        videoId = args['url'].split('watch?v=')[1]

        r = requests.get(buildYoutubeQueryURL(videoId))
        response = r.json()

        if len(response['items']) == 0:
            return buildResponse('Video not found', 404)

        youtubeDetails = response['items'][0]

        #At the time of this development the youtube API does not work properly to the embeddable property
        if not youtubeDetails['status']['embeddable']:
            return buildResponse('Video is not embeddable', 400)

        print youtubeDetails['snippet']['title']

        music = MusicModel()
        music.title = youtubeDetails['snippet']['title']
        music.description = youtubeDetails['snippet']['description']
        music.channel_title = youtubeDetails['snippet']['channelTitle']
        music.type = args['type']
        music.video_id = videoId
        music.save()

        return buildResponse('', 201)

    def put(self):

        self.parser.add_argument('action', help='Action is required', location='args')
        args = self.parser.parse_args()

        # get required action
        action = args['action'].upper()

        def reset():
            musics = MusicModel.objects().update(has_played=False)

        # switch
        options = {
            'RESET': reset
        }

        # if actions is not present in options object, then request was mal-formed
        if not action in options:
            return buildResponse('', 400)

        # execute action and save music
        options[action]()

        return buildResponse('', 200)

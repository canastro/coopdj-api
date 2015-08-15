import datetime
import bson
import requests
from flask import Flask, Response, json
from flask.ext.mongoengine import MongoEngine
from flask_restful import reqparse, abort, Api, Resource, inputs

from app.models import MusicModel

def buildResponse(data, status):
    return Response(json.dumps(data), status=status, mimetype='application/json')

# Musics
# shows a list of all todos, and lets you POST to add new tasks
class Musics(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Musics, self).__init__()

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
            type=inputs.regex('youtube\.com\/watch\?v=\w*'),
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

        #TODO: VALIDATE IF IS EMBBEDABLE
        #https://www.googleapis.com/youtube/v3/videos?part=status&id=RsT3ttYbtr0&key={YOUR_API_KEY}
        #http://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python
        r = requests.get("https://www.googleapis.com/youtube/v3/videos?part=status&id=" + videoId + "&key=AIzaSyCyuznWcYDV_ORT9d1ONltKy5OL8S441wM")
        response = r.json()

        print response

        if not response['items'][0]['status']['embeddable']:
            return buildResponse('Video is not embeddable', 400)

        music = MusicModel()
        music.type = args['type']
        music.url = videoId
        music.save()

        return buildResponse('', 201)

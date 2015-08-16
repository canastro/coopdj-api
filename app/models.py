import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

# http://docs.mongoengine.org/
class MusicModel(db.Document):
    id = db.SequenceField(primary_key=True, sequence_name='music_id')
    type = db.StringField(max_length=255, required=True)
    title = db.StringField(max_length=255, required=True)
    description = db.StringField()
    channel_title = db.StringField(max_length=255, required=True)
    video_id = db.StringField(max_length=255, required=True)
    votes = db.IntField(default=0)
    has_played = db.BooleanField(default=False)
    added_at = db.DateTimeField(default=datetime.datetime.now, required=True)

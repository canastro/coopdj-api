import unittest, mongoengine, json, app

from flask.ext.api import status
from app.models import MusicModel



def generateMusic(url):
    music = MusicModel()
    music.type = 'YOUTUBE'
    music.url = url
    music.save()

def removeMusic(url):
    music = MusicModel.objects.get(url=url).delete()

def voteMusicUp(url):
    music = MusicModel.objects.get(url=url)
    music.votes += 1
    music.save()

# Here's our "unit tests".
class Musics(unittest.TestCase):

    def setUp(self):

        app.init(
            MONGODB_SETTINGS={'DB': 'testing'},
            TESTING=True,
            CSRF_ENABLED=False
        )
        self.app = app.app.test_client()

        generateMusic('1')
        generateMusic('2')

    def tearDown(self):

        removeMusic('1')
        removeMusic('2')


    def test_get_all(self):
        response = self.app.get('/musics?action=all')
        jsonResponse = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(jsonResponse), 2)
        self.assertEqual(jsonResponse[0]['votes'], 0)
        self.assertEqual(jsonResponse[1]['votes'], 0)

        self.assertEqual(jsonResponse[0]['url'], '1')
        self.assertEqual(jsonResponse[1]['url'], '2')

    def test_get_next(self):

        voteMusicUp('2')

        response = self.app.get('/musics?action=NEXT')
        jsonResponse = json.loads(response.get_data(as_text=True))

        self.assertEqual(jsonResponse['votes'], 1)
        self.assertEqual(jsonResponse['url'], '2')

    def test_get_invalid_action(self):

        response = self.app.get('/musics?action=N')

        #http://www.flaskapi.org/api-guide/status-codes/#client-error-4xx
        self.assertTrue(status.is_client_error(response.status_code))

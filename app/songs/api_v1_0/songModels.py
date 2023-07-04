
from config import mongoengine

class Song(mongoengine.Document):
    tittle = mongoengine.StringField()
    artist = mongoengine.StringField()
    gender = mongoengine.StringField()
    url = mongoengine.StringField()
    user = mongoengine.StringField()

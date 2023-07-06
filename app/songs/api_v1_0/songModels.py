
from config import mongoengine

class Song(mongoengine.Document):
    title = mongoengine.StringField()
    artist = mongoengine.StringField()
    gender = mongoengine.StringField()
    favorite = mongoengine.BooleanField(default=False)
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField()
    user = mongoengine.StringField()

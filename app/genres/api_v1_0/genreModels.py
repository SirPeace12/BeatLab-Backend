from config import mongoengine 
from songs.api_v1_0.songModels import CreateUser


class CreateSong(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    title = mongoengine.StringField()
    artist = mongoengine.StringField()
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField()
    user = mongoengine.EmbeddedDocumentField(CreateUser)

class Genre(mongoengine.Document):
    description = mongoengine.StringField()
    songs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateSong))


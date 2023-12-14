from config import mongoengine
from songs.api_v1_0.songModels import CreateGenre


class userPlayList(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    nameUser = mongoengine.StringField()
    lastNameUser = mongoengine.StringField()
    email = mongoengine.StringField()
    phone = mongoengine.StringField()

class CreateSongPlayList(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    title = mongoengine.StringField()
    artist = mongoengine.StringField()
    genres = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateGenre))
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField()

class PlaylistSong(mongoengine.Document):
    playlistName = mongoengine.StringField()
    description = mongoengine.StringField()
    songs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateSongPlayList))
    user = mongoengine.EmbeddedDocumentField(userPlayList)

from config import mongoengine
from songs.api_v1_0.songModels import CreateGenre


class CreateSongUser(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    title = mongoengine.StringField()
    artist = mongoengine.StringField()
    genres = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateGenre))
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField()

class CreatePlayListUser(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    playlistName = mongoengine.StringField()
    description = mongoengine.StringField()
    songs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateSongUser))

class Users(mongoengine.Document):
    nameUser = mongoengine.StringField()
    lastNameUser = mongoengine.StringField()
    email = mongoengine.EmailField()
    password = mongoengine.StringField()
    phone = mongoengine.StringField()
    state = mongoengine.BooleanField()
    resetToken = mongoengine.StringField()
    userPhotoURL = mongoengine.StringField()
    playlist_songs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreatePlayListUser))
    songs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateSongUser))

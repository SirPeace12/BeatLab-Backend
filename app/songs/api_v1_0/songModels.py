from config import mongoengine

class CreateGenre(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    description = mongoengine.StringField()

class CreateUser(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField()
    nameUser = mongoengine.StringField()
    lastNameUser = mongoengine.StringField()
    email = mongoengine.StringField()
    phone = mongoengine.StringField()

class Song(mongoengine.Document):
    title = mongoengine.StringField()
    artist = mongoengine.StringField()
    genres = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CreateGenre))
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField()
    user = mongoengine.EmbeddedDocumentField(CreateUser)


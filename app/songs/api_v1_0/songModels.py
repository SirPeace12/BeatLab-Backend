
from config import mongoengine

class Song(mongoengine.Document):
    title = mongoengine.StringField(default="Desconocido")
    artist = mongoengine.StringField(default="Desconocido")
    gender = mongoengine.StringField(default="Desconocido")
    favorite = mongoengine.BooleanField(default=False)
    songURL = mongoengine.StringField()
    imageSongURL = mongoengine.StringField(default="https://i.postimg.cc/4NBdd9NF/Beat-Lab-Logo.png")
    user = mongoengine.StringField()

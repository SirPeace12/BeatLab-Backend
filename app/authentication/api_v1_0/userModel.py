
from config import mongoengine

class Users(mongoengine.Document):
    nameUser = mongoengine.StringField()
    lastNameUser = mongoengine.StringField()
    email = mongoengine.StringField()
    password = mongoengine.StringField()
    phone = mongoengine.StringField()
    state = mongoengine.BooleanField(default = True)
    resetToken = mongoengine.StringField()
    userPhotoURL = mongoengine.StringField(default="https://i.postimg.cc/4NBdd9NF/Beat-Lab-Logo.png")

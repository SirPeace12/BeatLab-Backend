
from config import mongoengine

class Users(mongoengine.Document):
    nameUser = mongoengine.StringField()
    lastNameUser = mongoengine.StringField()
    email = mongoengine.StringField()
    password = mongoengine.StringField()
    phone = mongoengine.StringField()
    state = mongoengine.BooleanField(default = True)
    resetToken = mongoengine.StringField()
    userPhotoURL = mongoengine.StringField(default="https://i.postimg.cc/rFn1FcCW/8d70112b-c384-42d9-b2bd-20e4adc500eb.jpg")

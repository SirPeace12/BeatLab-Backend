from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/BeatLab'
mongo = PyMongo(app)
db = mongo.db.users
db.create_index('email', unique=True)

urlBase = "http://localhost:5173/"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'miguelangelpazvelasco@gmail.com'
MAIL_PASSWORD = 'kipuququhwguajkp' 

MAIL_DEFAULT_SENDER = 'miguelangelpazvelasco1@gmail.com'
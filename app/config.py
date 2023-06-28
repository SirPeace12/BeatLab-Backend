from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI']='mongodb://localhost/BeatLab'
mongo = PyMongo(app)
db = mongo.db.users
db.create_index('email', unique=True)

urlBase = "http://localhost:5173/"


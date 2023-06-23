from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/SpotItunes'
mongo = PyMongo(app)
db = mongo.db.users


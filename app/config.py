from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app, methods=['GET', 'POST', 'PUT', 'DELETE'], supports_credentials=True, origins="*", allow_headers=["Content-Type"])
app.config['MONGO_URI']='mongodb://localhost:27017/BeatLab'
mongo = PyMongo(app)
db = mongo.db.users
db.create_index('email', unique=True)

urlBase = "http://localhost:5173/"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'info.beatlabapp@gmail.com'
MAIL_PASSWORD = 'dgmqncakzsmachsq' 

MAIL_DEFAULT_SENDER = 'miguelangelpazvelasco1@gmail.com'
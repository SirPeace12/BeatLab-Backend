from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from flask_cloudy import Storage
import mongoengine

from flask_redis import FlaskRedis


# inicializacion de la aplicacion
app = Flask(__name__)

# Conexion al servidor de las canciones en Microsoft BLOB storage
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=beatlabsql;AccountKey=JpYdCBjz//Uh4hTMEUjy8oIw3/MgyJWa+bhBt1quQtKDVKJpFw98AgUMuOT7xQbKj6o9zrO+Iqbw+AStlum3Qg==;EndpointSuffix=core.windows.net"
CONTAINER_NAME_SONG = "songs"
CONTAINER_NAME_IMAGES_SONG = "imagesong"
CONTAINER_NAME_IMAGES_USER = "imageuser"

# Conexion con el blob
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
# Conexion con los contenedores
container_client_song = blob_service_client.get_container_client(CONTAINER_NAME_SONG)
container_client_images_song = blob_service_client.get_container_client(CONTAINER_NAME_IMAGES_SONG)
container_client_images_user = blob_service_client.get_container_client(CONTAINER_NAME_IMAGES_USER)


# Conexion a la base de datos en MONGO
app.config['MONGO_URI']='mongodb://localhost:27017/BeatLab'
mongo = PyMongo(app)
db = mongo.db.users
dbSongs = mongo.db.songs
db.create_index('email', unique=True)
mongoengine.connect('BeatLab', host='localhost', port=27017)

# Conexion a redis
app.config['REDIS_URL'] = "redis://default:oxWSVaw6SAJadsrc7SqN2aiUrXsGvM2C@redis-15385.c326.us-east-1-3.ec2.cloud.redislabs.com:15385"
redis_client = FlaskRedis(app)

# Configuracion para enviar el correo de recuperacion
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'beatlab'
Session(app)

# Configuracion para enviar el correo de recuperacion

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'info.beatlabapp@gmail.com'
MAIL_PASSWORD = 'dgmqncakzsmachsq' 
MAIL_DEFAULT_SENDER = 'miguelangelpazvelasco1@gmail.com'

urlBase = "http://localhost:5173/"

CORS(app, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], supports_credentials=True, origins="*", allow_headers=["Content-Type"])

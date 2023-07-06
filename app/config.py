from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from flask_cloudy import Storage
import mongoengine

# inicializacion de la aplicacion
app = Flask(__name__)

# Conexion al servidor de las canciones en Microsoft BLOB storage
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=beatlab;AccountKey=wxtVr/zpbjPkihy/ysj528e4Af7eN5lpDvhNbBhmJyuG9kjzLlitGmlH/Mn9pkvGSMmpNchi/ygV+AStI1V2AQ==;EndpointSuffix=core.windows.net"
CONTAINER_NAME_SONG = "songs"
CONTAINER_NAME_IMAGES_SONG = "imagesong"
CONTAINER_NAME_IMAGES_USER = "imageuser"


blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
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


CORS(app, methods=['GET', 'POST', 'PUT', 'DELETE'], supports_credentials=True, origins="*", allow_headers=["Content-Type"])



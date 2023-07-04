

from flask import Flask, request,jsonify
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client, blob_service_client,CONTAINER_NAME 
from songModels import Song


def getContainerClient(file):
    return container_client.get_blob_client(file.filename)

def uploadServer(file):
    getContainerClient(file).upload_blob(file)

def generateSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME,
        blob_name = file.filename
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=1))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{file.filename}?{sas_token}"
    
def createSongDataBase(songData):
    Song(tittle = songData["name"],
          artist = songData["artist"],
          gender = songData["gender"],
          url = songData["gender"],
        #   user = songData["gender"],
          )



def upload():
    songData = {
        "name": request.json['name'],
        "artist": request.json['artist'],
        "gender": request.json['gender'],
        "file":  request.files['file'],
    }
    uploadServer(songData["file"])
    
    songURL = generateSongURL(songData["file"])

    return "Archivo cargado exitosamente en R2 de Cloudflare"

def play():
    userData = {
        "name":"prueba.mp3"
    }

    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=beatlab;AccountKey=wxtVr/zpbjPkihy/ysj528e4Af7eN5lpDvhNbBhmJyuG9kjzLlitGmlH/Mn9pkvGSMmpNchi/ygV+AStI1V2AQ==;EndpointSuffix=core.windows.net"
    CONTAINER_NAME = "songs"

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME,
        blob_name = userData['name'],
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=1)  # Expiración del token de SAS
    )
    file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{userData['name']}?{sas_token}"
    
    # return render_template('play_song.html', song_data=file_url)


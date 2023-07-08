from datetime import datetime, timedelta
from flask import jsonify, redirect, request, url_for
from flask_mail import Mail, Message
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from flask import session
from config import db, app
from authentication.api_v1_0.userModel import Users
from config import blob_service_client, container_client_images_user, CONTAINER_NAME_IMAGES_USER
import secrets
import string
import uuid

app.config.from_pyfile('config.py')

mail = Mail(app)

def uploadPhotoServer(file):
    container_client_images_user.get_blob_client(file.filename).upload_blob(file)

def newName(filename):
    return f"{str(uuid.uuid4())}_{filename}"

def generatePhotoSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME_IMAGES_USER,
        blob_name = file.filename,
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=720))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_IMAGES_USER}/{file.filename}?{sas_token}"

def savePhotoDataBase(email, imageUserURL):
    user = Users.objects(email = email).first()
    user.userPhotoURL = imageUserURL
    user.save()

def registered(userData):
    return False if not userData else True 

def validate(data, dbData):
    return data == dbData

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permitir todas las solicitudes de origen cruzado
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE, PATCH'  # Métodos permitidos
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # Encabezados permitidos
    return response

def handle_options_request():
    # Realizar acciones necesarias para la solicitud OPTIONS
    # ...
    return jsonify({'message': 'CORS preflight request'})


def login():
    if request.method == 'POST':
        userData = {
            "email": request.json["email"],
            "password": request.json["password"],
        }

        password = userData['password'] 
        email = userData['email']

        dbSearch = Users.objects(email = email).first()

        if (not registered(dbSearch)):
            dbEmail = None
            dbPassword = None
        else:
            dbEmail = dbSearch.email
            dbPassword = dbSearch.password

        if (not registered(dbEmail)):
            return jsonify({"LoginFailed" : "Usuario no registrado" })

        if (not validate(password, dbPassword)):
            return jsonify({"LoginFailed" : "Contraseña Incorrecta" })
    
        if (registered(dbEmail) and validate(password, dbPassword) and validate(email, dbEmail)):
            user = {
            'nameUser' : dbSearch.nameUser,
            'lastNameUser' : dbSearch.lastNameUser,
            'email' : dbSearch.email,
            'userPhotoURL' : dbSearch.userPhotoURL,
            }
            
            return jsonify({"LoginSuccessfull" : user})
        else: 
            return jsonify({"LoginFailed" : "Login Failed" })
    else:
        return handle_options_request()
    
def sendWelcomeEmail(emailUser):
    msg = Message('Bienvenido A BeatLab', recipients=[emailUser])
    msg.html = '''
    <html>
    <head>
        <style>
            h1 { color: #43046E; }
            p { font-size: 14px; }
        </style>
    </head>
        <body 
            style="background: #fff; display: flex; justify-content: center; align-items: center;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
        
        <div style="text-align: center; align-items: center;  justify-content: center;
        border: 4px solid #ebb8f2; padding: 20px; border-radius: 20px; ">
            <h1 style="font-size: 2.5rem; padding: 0px">
                ¡Bienvenido a BeatLab, x!
            </h1>
            <p style="  color: rgb(215, 82, 233);">
                -------------------------------------------------
            </p>
            <p>
                Tu destino musical definitivo para guardar y disfrutar de tus canciones favoritas en un solo lugar.
                Explora, crea y comparte melodías increíbles con otros amantes de la música.
            </p>
            <h2>
                ¡Gracias por unirte a nuestra aplicación para guardar canciones!
            </h2>
            <p>
                Esperamos que disfrutes de una experiencia musical única con BeatLab.
            </p>
            <img src="https://i.postimg.cc/4NBdd9NF/Beat-Lab-Logo.png" width="300" height="300">
        
            <div style="align-items: center; justify-content: center; display:flex;">
                <p style="  color: rgb(94, 35, 102);">
                    Developed by Raccoon Soft
                </p>
                <img src="https://i.postimg.cc/dtH595VR/Racoon-Soft-Logo.webp" width="16" height="16" style="margin-left: 3px">
            </div>
        </div>
        

    </body>
    </html>
    '''
    mail.send(msg)

def creeateUser(userData):
    user = Users(nameUser = userData["nameUser"],
                lastNameUser = userData["lastNameUser"],
                email = userData["email"],
                password = userData["password"],
                phone = userData["phone"],
                )
    user.save()
    
def register():
    userData = {
        "nameUser": request.json["nameUser"],
        "lastNameUser": request.json["lastNameUser"],
        "email": request.json["email"],
        "password": request.json["password"],
        "phone": request.json["phone"]
    }

    dbSearch = Users.objects(email = userData["email"])

    if (not registered(dbSearch)):
        creeateUser(userData)
        sendWelcomeEmail(userData['email'])
        return jsonify({"Register" : "Register Successful" })
    else:
        return jsonify({"Register" : "Registered User" })

def generateToken(length):
    characters = string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token

def sendRecuperationEmail():
    userData = {
        "email": request.json["email"],
    }

    emailUser = userData["email"]
    user = Users.objects(email = emailUser).first()

    if (user == None):
        return jsonify({"RecuperationEmail": "Email Sent Failed"})

    token = generateToken(6)
    msg = Message('Recuperación de contraseña', recipients=[emailUser])
    msg.body = f'Hola, has solicitado restablecer tu contraseña. Su codigo de recuperacion es: {token}'
    mail.send(msg)
    user.resetToken = token
    user.save()
    return jsonify({"RecuperationEmail": "Email Sent Successfully"})

def savePassword(userData, tokenUser):

    newPassword = userData["newPassword"]
    confirm_password = userData["confirmPassword"]

    if (tokenUser):
        if(newPassword == confirm_password):
            user = Users.objects(resetToken = tokenUser).first()
            user.password = newPassword
            user.resetToken = ""
            user.save()
        else:
            return jsonify ({"resetPassword": "Passwords Do Not Match"})

    return jsonify ({"resetPassword": "Change Password Successfull"})

def confirmToken():
    tokenData = {
        "token" : request.json["token"],
    }
    token = tokenData["token"]

    tokenUser = Users.objects(resetToken=token)

    if (registered(tokenUser)):
        return jsonify ({"Correct Token" : token})
    else:
        return jsonify ({"token" : "Incorrect Token"})

def resetPassword(token):
    
    userData = {
        "newPassword":request.json["newPassword"],
        "confirmPassword":request.json["confirmPassword"]
        }
    
    savePassword(userData,token)

    return jsonify({"resetPassword" : "Change Password Successfull"})
        
def uploadPhoto(email):
    userData = {
        "fileImageUser":  request.files['fileImageUser'],
    }

    userData["fileImageUser"].filename = newName(userData["fileImageUser"].filename)

    uploadPhotoServer(userData["fileImageUser"])

    imageUserURL = generatePhotoSongURL(userData["fileImageUser"])

    savePhotoDataBase(userData,email ,imageUserURL)

    return jsonify({'PhotoUser' : "Photo Uploaded Successful"})

def updateName(email):
    userData = {
        "name":  request.json['name'],
    }

    user = Users.objects(email = email).first()
    user.nameUser = userData["name"]
    user.save()

    return jsonify({"updateName" : "updateName Successful"})

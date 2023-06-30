from flask import Flask, jsonify, redirect, request, url_for
from flask_pymongo import PyMongo,ObjectId
from flask_mail import Mail, Message
from config import db, app
import secrets
app.config.from_pyfile('config.py')

mail = Mail(app)

def registered(userData):
    return False if userData == None else True 

def validate(data, dbData):
    return data == dbData

def login():
    userData = {
        "email": request.json["email"],
        "password": request.json["password"],
    }

    password = userData['password'] 
    email = userData['email']

    dbSearch = db.find_one({'email':email})

    if (dbSearch is None):
        dbEmail = None
        dbPassword = None
    else:
        dbEmail = dbSearch["email"]
        dbPassword = dbSearch["password"]

    if (registered (dbEmail)):
        return jsonify({"Login" : "Registerd User" })
    elif (validate(password, dbPassword) and validate(email, dbEmail)):
        return jsonify({"Login" : "Login Successfull"})
    else: 
        return jsonify({"Login" : "Login Failed" })

def register():
    userData = {
        "nameUser": request.json["nameUser"],
        "lastNameUser": request.json["lastNameUser"],
        "email": request.json["email"],
        "password": request.json["password"],
        "phone": request.json["phone"],
        "state":True
    }
    dbSearch = db.find_one({'email':userData['email']})
    
    if (not registered(dbSearch)):
        db.insert_one(userData)
        return jsonify({"Register" : "Register Successful" })
    else:
        return jsonify({"Register" : "Registered User" })
    
def sendRecuperationEmail():
    userData = {
        "email":request.json["email"]
    }

    emailUser = userData["email"]

    # token1 = random(000000 , 999999)

    token = secrets.token_hex(16)
    reset_url = url_for('auth.resetPassword', token=token, _external=True)
    msg = Message('Recuperación de contraseña', recipients=[emailUser])
    msg.body = f'Hola, has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para restablecerla: {reset_url}'
    mail.send(msg)

    db.update_one({"email" : userData["email"]}, {'$set': {"resetToken": token}})
    return jsonify({"Recuperation Email": "Email Sent Successfull"})

def savePassword(userData, tokenUser):

    newPassword = userData["newPassword"]
    confirm_password = userData["confirmPassword"]

    if (tokenUser):
        if(newPassword == confirm_password):
            db.update_one({'resetToken': tokenUser["token"]}, {'$set': {'password': newPassword}})
        else:
            return jsonify ({"resetPassword": "Passwords do not match"})

    return jsonify ({"resetPassword": "Change Password Successfull"})

def resetPassword(token):
    tokenUser = db.find_one({'resetToken': token})
    if request.method == 'POST':
        userData = {
            "newPassword":request.json["newPassword"],
            "confirmPassword":request.json["confirmPassword"]
        }
        savePassword(userData, tokenUser)
        print(token)
        return jsonify ({"resetPassword": "Change Password Successfull"})
    
    if (tokenUser):
        return redirect("http://localhost:5173/", code=302)
    return jsonify ({"resetPassword": "Change Password Failed"})

def confirmToken():
    userData = {
            "token":request.json["token"]
        }
    
    token = userData["token"]

    user = db.find_one({ "resetToken": token })

    print(user)

    return jsonify ({"resetPassword": "Change Password Failed"})


    
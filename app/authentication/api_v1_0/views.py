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
    if (not registered(userData["email"])):
        result = db.insert_one(userData)
        return jsonify({"Register" : "Register Successful" })
    else:
        return jsonify({"Register" : "Register Failed" })


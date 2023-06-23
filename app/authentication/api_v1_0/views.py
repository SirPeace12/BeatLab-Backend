from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId
from config import db


def login():
    userData = {
        "username": request.json["username"],
        "password": request.json["password"],
    }
    isLogged = False if db.find_one({"name": userData["username"]}) is None else True 
    
    if (isLogged ):
        return jsonify({"Login" : "Login Successful" })
    else:
        return jsonify({"Login" : "Login Failed" })
    
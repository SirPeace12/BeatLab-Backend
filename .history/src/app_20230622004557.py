from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/prueba'
mongo = PyMongo(app)

bd = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    print(request.json)
    return 'received'

@app.route('/users', methods=['GET'])
def getUsers():
    print(request.json)
    return 'received'

@app.route('/users/<id>', methods=['GET'])
def getUser():
    print(request.json)
    return 'received'

if __name__=="__main__":
    app.run(debug=True)
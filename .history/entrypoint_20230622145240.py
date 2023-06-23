 
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/SpotItunes'
mongo = PyMongo(app)

db = mongo.db.users
@app.route('/')
def index():
    return '<h1>holaaa<h1>'


@app.route('/users', methods=['POST'])
def createUser():
    user_data = {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }
    result = db.insert_one(user_data)
    return jsonify(str(result.inserted_id))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': str(ObjectId(doc['name'])),
            'email': str(ObjectId(doc['email'])),
            'password': str(ObjectId(doc['password'])),
        })
    db.find()
    return jsonify(str(result.inserted_id))

if __name__=="__main__":
    app.run(debug=True)
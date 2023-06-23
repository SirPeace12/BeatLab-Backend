from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/SpotItunes'
mongo = PyMongo(app)
collection = mongo.db['users']
documents = collection.find()  # Obtener todos los documentos de la colección
for doc in documents:
    print(doc)
# print(mongo)
# print(collection)


bd = mongo.db.users
@app.route('/')
def index():

    return '<h1>holaaa<h1>'


@app.route('/users', methods=['POST'])
def createUser():
    print(request.json)
    return 'received'

if __name__=="__main__":
    app.run(debug=True)
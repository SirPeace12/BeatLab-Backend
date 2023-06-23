from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&app'
mongo = PyMongo(app)

db = mongo.db  # Obtiene la referencia a la base de datos

@app.route('/')
def index():
    return '<h1>holaaa<h1>'

@app.route('/users', methods=['POST'])
def createUser():
    collection = db.users  # Obtiene la referencia a la colección "users"

    print(request.json)
    return 'received'

if __name__ == "__main__":
    app.run(debug=True)

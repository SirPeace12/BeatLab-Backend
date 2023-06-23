from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/SpotItunes'
mongo = PyMongo(app)

try:
    bd = mongo.db.users
except ConnectionError as e:
    print("Error connecting to MongoDB:", str(e))
@app.route('/')
def index():
    return '<h1>holaaa<h1>'

@app.route('/users', methods=['POST'])
def createUser():
    
    print(request.json)
    return 'received'

if __name__=="__main__":
    app.run(debug=True)
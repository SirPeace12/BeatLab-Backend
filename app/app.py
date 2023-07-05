import config 
app = config.app

from authentication.api_v1_0.routes import auth_routes
from songs.api_v1_0.routes import songs_routes

app.register_blueprint(auth_routes)
app.register_blueprint(songs_routes)

@app.route('/')
def index():
    return config.urlBase


# @app.route('/users', methods=['POST'])
# def createUser():
#     user_data = {
#         'name': request.json['name'],
#         'email': request.json['email'],
#         'password': request.json['password']
#     }
#     result = db.insert_one(user_data)
#     return jsonify(str(result.inserted_id))

# @app.route('/users', methods=['GET'])
# def getUsers():
#     users = []
#     for doc in db.find():
#         users.append({
#             '_id': str(ObjectId(doc['_id'])),
#             'name': doc['name'],
#             'email': doc['email'],
#             'password': doc['password']
#         })
#     return jsonify(users)

# @app.route('/user/<id>', methods=['GET'])
# def getUser(id):
#     user = db.find_one({'_id':ObjectId(id)})
#     return jsonify({
#         '_id': str(ObjectId(user['_id'])),
#         'name': user['name'],
#         'email': user['email'],
#         'password': user['password']
#     })

# @app.route('/users/<id>', methods=['PUT'])
# def updateUser(id):
#     db.update_one({'_id' : ObjectId(id)},{'$set':{
#         'name': request.json['name'],
#         'email': request.json['email'],
#         'password': request.json['password']
#     }})
#     return jsonify({"msg": "User updated"})


if __name__=="__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/spotify_clone'
mongo = PyMongo(app)

# Modelo
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def save(self):
        mongo.db.songs.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        songs = mongo.db.songs.find()
        output = []
        for song in songs:
            output.append({'title': song['title'], 'artist': song['artist']})
        return output

    @staticmethod
    def delete(song_id):
        mongo.db.songs.delete_one({'_id': song_id})

# Controlador
@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.get_all()
    return jsonify({'songs': songs})

@app.route('/songs', methods=['POST'])
def add_song():
    title = request.json['title']
    artist = request.json['artist']
    new_song = Song(title, artist)
    new_song.save()
    return jsonify({'message': 'Song added successfully'})

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    Song.delete(song_id)
    return jsonify({'message': 'Song deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

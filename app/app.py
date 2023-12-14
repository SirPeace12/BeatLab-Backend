import config 
app = config.app

from authentication.api_v1_0.routes import auth_routes
from songs.api_v1_0.routes import songs_routes
from genres.api_v1_0.routesGenres import genres_routes
from play_list.api_v1_0.routesPlayList import playList_routes

app.register_blueprint(auth_routes)
app.register_blueprint(songs_routes)
app.register_blueprint(genres_routes)
app.register_blueprint(playList_routes)

@app.route('/')
def index():
    return config.urlBase

if __name__=="__main__":
    app.run(debug=True)
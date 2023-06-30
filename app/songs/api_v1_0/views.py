import pyrebase

# storage.child
def upload():
    config = {
        "apiKey": "AIzaSyArp7cqUqdpDkgZarHU7VwNvXMssqUpaqM",
        "authDomain": "beatlab-d0d05.firebaseapp.com", 
        "databaseURL": "https://beatlab-d0d05-default-rtdb.firebaseio.com",
        "projectId": "beatlab-d0d05",
        "storageBucket": "beatlab-d0d05.appspot.com",
        "messagingSenderId": "409746057896",
        "appId": "1:409746057896:web:bc2d3411fc8287bd94f09d",
        "measurementId": "G-SDTXRL107Y",
        "serviceAccount":"serviceAccountKey.json"
    };

    firebaseStorage = pyrebase.initialize_app(config)
    storage = firebaseStorage.storage()


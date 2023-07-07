from flask import jsonify, redirect, request, url_for
from flask_mail import Mail, Message
from flask import session
from config import db, app
import secrets

app.config.from_pyfile('config.py')

mail = Mail(app)

def registered(userData):
    return False if userData == None else True 

def validate(data, dbData):
    return data == dbData

def login():
    print("11111")
    
    userData = {
        "email": request.json["email"],
        "password": request.json["password"],
    }

    password = userData['password'] 
    email = userData['email']

    dbSearch = db.find_one({'email':email})


    if (dbSearch is None):
        dbEmail = None
        dbPassword = None
    else:
        dbEmail = dbSearch["email"]
        dbPassword = dbSearch["password"]

    if (not registered(dbEmail)):
        return jsonify({"LoginFailed" : "Usuario no registrado" })

    if (not validate(password, dbPassword)):
        return jsonify({"LoginFailed" : "Contraseña Incorrecta" })
    

    if (registered(dbEmail) and validate(password, dbPassword) and validate(email, dbEmail)):
        user = {
        'nameUser' : dbSearch['nameUser'],
        'lastNameUser' : dbSearch['lastNameUser'],
        'email' : dbSearch['email']
        }
        print(user)
        print("-----------------------")
        session['user'] = user["email"]
        print(session.get('user'))
        return jsonify({"LoginSuccessfull" : user})
    else: 
        return jsonify({"LoginFailed" : "Login Failed" })
    
def sendWelcomeEmail(emailUser):
    msg = Message('Bienvenido A BeatLab', recipients=[emailUser])
    msg.html = '''
    <html>
    <head>
        <style>
            h1 { color: #43046E; }
            p { font-size: 14px; }
        </style>
    </head>
        <body 
            style="background: #fff; display: flex; justify-content: center; align-items: center;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
        
        <div style="text-align: center; align-items: center;  justify-content: center;
        border: 4px solid #ebb8f2; padding: 20px; border-radius: 20px; ">
            <h1 style="font-size: 2.5rem; padding: 0px">
                ¡Bienvenido a BeatLab, x!
            </h1>
            <p style="  color: rgb(215, 82, 233);">
                -------------------------------------------------
            </p>
            <p>
                Tu destino musical definitivo para guardar y disfrutar de tus canciones favoritas en un solo lugar.
                Explora, crea y comparte melodías increíbles con otros amantes de la música.
            </p>
            <h2>
                ¡Gracias por unirte a nuestra aplicación para guardar canciones!
            </h2>
            <p>
                Esperamos que disfrutes de una experiencia musical única con BeatLab.
            </p>
            <img src="https://i.postimg.cc/4NBdd9NF/Beat-Lab-Logo.png" width="300" height="300">
        
            <div style="align-items: center; justify-content: center; display:flex;">
                <p style="  color: rgb(94, 35, 102);">
                    Developed by Raccoon Soft
                </p>
                <img src="https://i.postimg.cc/dtH595VR/Racoon-Soft-Logo.webp" width="16" height="16" style="margin-left: 3px">
            </div>
        </div>
        

    </body>
    </html>
    '''
    mail.send(msg)
    
def register():
    userData = {
        "nameUser": request.json["nameUser"],
        "lastNameUser": request.json["lastNameUser"],
        "email": request.json["email"],
        "password": request.json["password"],
        "phone": request.json["phone"],
        "state":True
    }
    dbSearch = db.find_one({'email':userData['email']})
    
    if (not registered(dbSearch)):
        db.insert_one(userData)
        sendWelcomeEmail(userData['email'])
        return jsonify({"Register" : "Register Successful" })
    else:
        return jsonify({"Register" : "Registered User" })
    
def logout():
    session.clear()
    return jsonify({"Logout": "UserLogout"})

def sendRecuperationEmail():
    userData = {
        "email":request.json["email"]
    }

    emailUser = userData["email"]

    # token1 = random(000000 , 999999)

    token = secrets.token_hex(16)
    reset_url = url_for('auth.resetPassword', token=token, _external=True)
    msg = Message('Recuperación de contraseña', recipients=[emailUser])
    msg.body = f'Hola, has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para restablecerla: {reset_url}'
    mail.send(msg)

    db.update_one({"email" : userData["email"]}, {'$set': {"resetToken": token}})
    return jsonify({"RecuperationEmail": "Email Sent Successfull"})

def savePassword(userData, tokenUser):

    newPassword = userData["newPassword"]
    confirm_password = userData["confirmPassword"]

    if (tokenUser):
        if(newPassword == confirm_password):
            db.update_one({'resetToken': tokenUser["token"]}, {'$set': {'password': newPassword}})
        else:
            return jsonify ({"resetPassword": "Passwords Do Not Match"})

    return jsonify ({"resetPassword": "Change Password Successfull"})

def resetPassword(token):
    tokenUser = db.find_one({'resetToken': token})
    if request.method == 'POST':
        userData = {
            "newPassword":request.json["newPassword"],
            "confirmPassword":request.json["confirmPassword"]
        }
        savePassword(userData, tokenUser)
        return jsonify ({"resetPassword": "Change Password Successfull"})
    
    if (tokenUser):
        return redirect("http://localhost:5173/", code=302)
    return jsonify ({"resetPassword": "ChangePasswordFailed"})

def confirmToken():
    userData = {
            "token":request.json["token"]
        }
    
    token = userData["token"]

    user = db.find_one({ "resetToken": token })

    print(user)

    return jsonify ({"resetPassword": "ChangePasswordFailed"})


    
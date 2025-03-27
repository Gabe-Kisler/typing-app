from flask import Flask
from firebase_admin import credentials, initialize_app, firestore


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretKey'


    cred = credentials.Certificate('app/credentials/Credentials.json')
    initialize_app(cred)


    from app.routes import routes_bp
    from app.auth import auth_bp


    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)


    return app

from flask import Flask
from firebase_admin import credentials, initialize_app, firestore
import os, json

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

    if firebase_credentials:
        cred = credentials.Certificate(json.loads(firebase_credentials))
    
    initialize_app(cred)


    from app.routes import routes_bp
    from app.auth import auth_bp


    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)


    return app

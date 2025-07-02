from flask import Flask
from app.config import Config as AppConfig
from app.extensions import db
from app.routes.root_route import register_all_routes

def create_app():
    app = Flask(__name__)
    config = AppConfig()  # Instantiate the settings class

    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = config.SECRET_KEY

    db.init_app(app)
    register_all_routes(app)

    return app

from flask import Flask
from app.config import Config as AppConfig
from app.extensions import db, jwt
from app.exceptionhandler.error_handler import register_jwt_error_handlers
from app.routes.root_route import register_all_routes

def create_app():
    app = Flask(__name__)
    config = AppConfig()  # Instantiate the settings class
    app.config.from_object(config)  # Load configuration from the class


    # app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    # app.config["SECRET_KEY"] = config.SECRET_KEY
    # app.config.update(
    #     SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
    #     SQLALCHEMY_TRACK_MODIFICATIONS=config.SQLALCHEMY_TRACK_MODIFICATIONS,
    #     SECRET_KEY=config.SECRET_KEY,
    #     JWT_SECRET_KEY=config.JWT_SECRET_KEY,
    #     JWT_TOKEN_LOCATION=config.JWT_TOKEN_LOCATION,
    #     JWT_HEADER_NAME=config.JWT_HEADER_NAME,
    #     JWT_HEADER_TYPE=config.JWT_HEADER_TYPE,
    # )

    
    db.init_app(app)
    jwt.init_app(app)
    register_jwt_error_handlers(jwt,app)
    
    register_all_routes(app)
    print("Loaded config:", {k: v for k, v in app.config.items() if k.startswith("JWT") or k.startswith("SQL")})


    return app

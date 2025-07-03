from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
def register_jwt_error_handlers(jwt: JWTManager, app):
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(error):
        return jsonify({"error": "Authorization header missing","message":str(error)}), 401
   
from flask import Flask, Blueprint

# Import sub-blueprints (no url_prefix in them now!)
from app.routes.user_route import user_blueprint
from app.routes.role_route import role_blueprint
from app.routes.asset_route import asset_blueprint

# Create common parent blueprint for /api
api = Blueprint("api", __name__, url_prefix="/api")

# Nest child blueprints
api.register_blueprint(user_blueprint, url_prefix="/users")
api.register_blueprint(role_blueprint, url_prefix="/roles")
api.register_blueprint(asset_blueprint, url_prefix="/assets")

def register_all_routes(app: Flask):
    app.register_blueprint(api)

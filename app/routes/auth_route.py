# app/routes/auth_route.py

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User_tbl
from app.extensions import db
from app.utils.create_jwt import create_jwt_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("Received login data:", data)

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = User_tbl.query.filter_by(email=data["email"]).first()
    
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_jwt_token(user.id, user.email)

    response = {
        "id": user.id,
        "email": user.email,
        "role": user.role.to_dict() if user.role else None,
        "jwt_token": token
    }

    return jsonify(response), 200

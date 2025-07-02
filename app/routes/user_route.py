from flask import Blueprint, jsonify, request
from flask_injector import inject
from app.services.user_service import UserService
from app.models.user import User

user_blueprint = Blueprint("user_routes", __name__)  # No url_prefix here; handled in root_routes.py

@user_blueprint.route("/", methods=["GET"])
@inject
def get_all_users(user_service: UserService):
    users = user_service.get_users()
    return jsonify([{
        "id": u.id,
        "name": u.name,
        "email": u.email
    } for u in users])

@user_blueprint.route("/<int:user_id>", methods=["GET"])
@inject
def get_user_by_id(user_id, user_service: UserService):
    user = user_service.get_user(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/", methods=["POST"])
@inject
def create_user(user_service: UserService):
    data = request.get_json()
    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        age=data.get("age"),
        is_active=data.get("is_active", True),
        role_id=data.get("role_id")
    )
    user = user_service.create_user(new_user)
    return jsonify({"id": user.id}), 201

@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@inject
def update_user(user_id, user_service: UserService):
    data = request.get_json()
    updated = user_service.update_user(user_id, data)
    if updated:
        return jsonify({"message": "User updated"})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@inject
def delete_user(user_id, user_service: UserService):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/search", methods=["GET"])
@inject
def search_user(user_service: UserService):
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email query param is required"}), 400

    user = user_service.search_user_by_email(email)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "is_active": user.is_active,
            "role_id": user.role_id
        }), 200
    return jsonify({"error": "User not found"}), 404


@user_blueprint.route("/paginated", methods=["GET"])
@inject
def get_users_paginated(user_service: UserService):
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    paginated_users = user_service.get_users_paginated(page, per_page)

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": paginated_users.total,
        "pages": paginated_users.pages,
        "data": [{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "age": u.age,
            "is_active": u.is_active,
            "role_id": u.role_id
        } for u in paginated_users.items]
    }), 200

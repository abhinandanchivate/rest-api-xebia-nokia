from flask import Blueprint, jsonify, request
from flask_injector import inject
from pydantic import ValidationError
# @jwtrequired
from flask_jwt_extended import jwt_required

from app.services.user_service import UserService
from app.models.user import User_tbl as User
from app.utils.create_jwt import create_jwt_token
from app.schemas.user_schema import UserCreateReq,UserResponseSchema
user_blueprint = Blueprint("user_routes", __name__)  # No url_prefix here; handled in root_routes.py



@user_blueprint.route("/", methods=["GET"])
@inject
@jwt_required()  # Ensure that this route requires a valid JWT token
def get_all_users(user_service: UserService):
    users = user_service.get_all_users()
    return jsonify([{
        "id": u.id,
        "name": u.name,
        "email": u.email
    } for u in users])

@user_blueprint.route("/<int:user_id>", methods=["GET"])
@inject
@jwt_required()
def get_user_by_id(user_id, user_service: UserService):
    
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/", methods=["POST"])
@inject
def create_user(user_service: UserService):

    try:
        data = request.get_json()
        user_data = UserCreateReq(**data)

        new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password"),
        age=data.get("age"),
        is_active=data.get("is_active", True),
        role_id=data.get("role_id")
    )
        new_user.set_password(user_data.password)  # Hash the password before saving
        user = user_service.create_user(new_user)
        # user_dict = {
        #     "id": user.id,
        #     "name": user.name,
        #     "email": user.email,
        #     "age": user.age,
        #     "is_active": user.is_active,
        #     "role_id": user.role_id,
        #     "created_at": user.created_at,
        #     "updated_at": user.updated_at
        # }
        user_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns}
        # add jwt token to user_dict
        user_dict["jwt_token"] = create_jwt_token(email=user_dict.get('email'),user_id=user_dict.get('id')) # Assuming get_jwt_token is a method in User model

        # print(user.__dict__)
        # user_dict = {key: value for key, value in user.__dict__.items() if not key.startswith('_')}

        user_response = UserResponseSchema.model_validate(user_dict).model_dump() # Convert to dict for JSON response
            # (
            # id=user.id,
            # name=user.name,
            # email=user.email,
            # age=user.age,
            # is_active=user.is_active,
            # role_id=user.role_id)
        return jsonify(user_response), 201
    except ValidationError as ve:
        # Format validation error into a user-friendly structure
        error_messages = {
            "error": [{"field": e['loc'], "message": e['msg']} for e in ve.errors()]
        }
        return jsonify(error_messages), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@inject
@jwt_required()
def update_user(user_id, user_service: UserService):
    data = request.get_json()
    updated = user_service.update_user(user_id, data)
    if updated:
        return jsonify({"message": "User updated"})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@inject
@jwt_required()
def delete_user(user_id, user_service: UserService):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/search", methods=["GET"])
@inject
@jwt_required()
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
@jwt_required()
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

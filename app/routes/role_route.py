from flask import Blueprint, jsonify, request
from flask_injector import inject
from flask_jwt_extended import jwt_required
from app.services.role_service import RoleService
from app.models.role import Role
from app.middleware.permissions import permission_required
role_blueprint = Blueprint("role_routes", __name__)  # Mounted under /api/roles

@role_blueprint.route("/", methods=["GET"])
@inject
@jwt_required()
def get_all_roles(role_service: RoleService):
    roles = role_service.get_all_roles()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "level": r.level,
        "created_at": r.created_at.isoformat()
    } for r in roles]), 200

@role_blueprint.route("/<int:role_id>", methods=["GET"])
@inject
@jwt_required()
def get_role_by_id(role_id, role_service: RoleService):
    role = role_service.get_role_by_id(role_id)
    if role:
        return jsonify({
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "level": role.level,
            "created_at": role.created_at.isoformat()
        }), 200
    return jsonify({"error": "Role not found"}), 404

@role_blueprint.route("/", methods=["POST"])
@inject
@jwt_required()
@permission_required("create")  # Assuming you have a permission for creating roles
def create_role(role_service: RoleService):
    data = request.get_json()
    new_role = Role(
        name=data.get("name"),
        description=data.get("description"),
        level=data.get("level"),
        permissions=data.get("permissions"),  # Assuming permission is a json
    )
    role = role_service.create_role(new_role)
    if role:
        return jsonify({"message": "Role created", "role": role.to_dict()}), 201
    return jsonify({"error": "Failed to create role"}), 400

@role_blueprint.route("/<int:role_id>", methods=["PUT"])
@inject
@jwt_required()
def update_role(role_id, role_service: RoleService):
    data = request.get_json()
    updated = role_service.update_role(role_id, data)
    if updated:
        return jsonify({"message": "Role updated"}), 200
    return jsonify({"error": "Role not found"}), 404

@role_blueprint.route("/<int:role_id>", methods=["DELETE"])
@inject
@jwt_required()
def delete_role(role_id, role_service: RoleService):
    success = role_service.delete_role(role_id)
    if success:
        return jsonify({"message": "Role deleted"}), 204
    return jsonify({"error": "Role not found"}), 404

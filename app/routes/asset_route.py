from flask import Blueprint, jsonify, request
from flask_injector import inject
from flask_jwt_extended import jwt_required
from app.services.asset_service import AssetService
from app.models.asset import Asset

asset_blueprint = Blueprint("asset_routes", __name__)  # Mounted under /api/assets

@asset_blueprint.route("/", methods=["GET"])
@inject
@jwt_required()
def get_all_assets(asset_service: AssetService):
    assets = asset_service.get_all_assets()
    return jsonify([{
        "id": a.id,
        "name": a.name,
        "category": a.category,
        "value": a.value,
        "purchase_date": a.purchase_date.isoformat() if a.purchase_date else None,
        "user_id": a.user_id
    } for a in assets]), 200

@asset_blueprint.route("/<int:asset_id>", methods=["GET"])
@inject
@jwt_required()
def get_asset_by_id(asset_id, asset_service: AssetService):
    asset = asset_service.get_asset_by_id(asset_id)
    if asset:
        return jsonify({
            "id": asset.id,
            "name": asset.name,
            "category": asset.category,
            "value": asset.value,
            "purchase_date": asset.purchase_date.isoformat() if asset.purchase_date else None,
            "user_id": asset.user_id
        }), 200
    return jsonify({"error": "Asset not found"}), 404

@asset_blueprint.route("/", methods=["POST"])
@inject
@jwt_required()
def create_asset(asset_service: AssetService):
    data = request.get_json()
    new_asset = Asset(
        name=data.get("name"),
        category=data.get("category"),
        value=data.get("value"),
        purchase_date=data.get("purchase_date"),
        user_id=data.get("user_id")
    )
    asset = asset_service.create_asset(new_asset)
    if asset:
        return jsonify({"message": "Asset created", "id": asset.id}), 201
    return jsonify({"error": "Failed to create asset"}), 400

@asset_blueprint.route("/<int:asset_id>", methods=["PUT"])
@inject
@jwt_required()
def update_asset(asset_id, asset_service: AssetService):
    data = request.get_json()
    updated = asset_service.update_asset(asset_id, data)
    if updated:
        return jsonify({"message": "Asset updated"}), 200
    return jsonify({"error": "Asset not found"}), 404

@asset_blueprint.route("/<int:asset_id>", methods=["DELETE"])
@inject
@jwt_required()
def delete_asset(asset_id, asset_service: AssetService):
    success = asset_service.delete_asset(asset_id)
    if success:
        return jsonify({"message": "Asset deleted"}), 204
    return jsonify({"error": "Asset not found"}), 404

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import public_user
from ..services import demo_store

citizen_bp = Blueprint("citizen", __name__)


@citizen_bp.get("/citizens/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = next((u for u in demo_store.USERS_BY_EMAIL.values() if u["id"] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "Citizen account not found."}), 404
    return jsonify({"success": True, "citizen": public_user(user)})


@citizen_bp.get("/documents")
@jwt_required()
def documents():
    return jsonify({"success": True, "items": [], "message": "No documents uploaded in this integration milestone."})


@citizen_bp.get("/applications")
@jwt_required()
def applications():
    return jsonify({"success": True, "items": [], "message": "Application API will be connected in a later milestone."})

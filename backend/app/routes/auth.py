import re
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from ..services import demo_store

auth_bp = Blueprint("auth", __name__)


def fail(message, status=400):
    return jsonify({"success": False, "message": message}), status


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("full_name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    mobile = str(data.get("mobile", "")).strip()
    password = str(data.get("password", ""))
    if len(name) < 2 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return fail("Enter a valid name and email address.")
    if not re.fullmatch(r"[0-9]{10}", mobile):
        return fail("Mobile number must contain exactly 10 digits.")
    if len(password) < 8:
        return fail("Password must contain at least 8 characters.")
    if email in demo_store.USERS_BY_EMAIL or mobile in demo_store.USERS_BY_MOBILE:
        return fail("An account with this email or mobile already exists.", 409)
    user = demo_store.create_user({
        "full_name": name,
        "email": email,
        "mobile": mobile,
        "password_hash": generate_password_hash(password),
        "is_verified": False,
        "citizen_id": None,
    })
    otp = current_app.config["DEMO_OTP"]
    demo_store.OTP_BY_USER[user["id"]] = otp
    response = {"success": True, "message": "Demo OTP created. Verify it to activate this demo account.", "otp_required": True}
    if current_app.config["APP_MODE"] == "demo":
        response["demo_otp"] = otp
    return jsonify(response), 201


@auth_bp.post("/otp/verify")
def verify_otp():
    data = request.get_json(silent=True) or {}
    identity = str(data.get("identity", "")).strip()
    otp = str(data.get("otp", "")).strip()
    user = demo_store.find_user(identity)
    if not user:
        return fail("No pending account found for that email or mobile.", 404)
    expected = demo_store.OTP_BY_USER.get(user["id"])
    if not expected or otp != expected:
        return fail("The demo OTP is incorrect or no longer valid.", 400)
    user["is_verified"] = True
    # The permanent demo Citizen ID is created only after successful contact verification.
    user["citizen_id"] = "CID-" + user["id"].replace("-", "")[:4].upper() + "-" + user["id"].replace("-", "")[4:8].upper() + "-" + user["id"].replace("-", "")[8:12].upper()
    demo_store.OTP_BY_USER.pop(user["id"], None)
    token = create_access_token(identity=user["id"])
    return jsonify({"success": True, "message": "Demo contact verification completed.", "access_token": token, "citizen": public_user(user)})


def public_user(user):
    return {"id": user["id"], "full_name": user["full_name"], "email": user["email"], "mobile": user["mobile"], "is_verified": user["is_verified"], "citizen_id": user["citizen_id"]}


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    identity = str(data.get("identity", "")).strip()
    password = str(data.get("password", ""))
    user = demo_store.find_user(identity)
    if not user or not check_password_hash(user["password_hash"], password):
        return fail("Invalid email/mobile or password.", 401)
    if not user["is_verified"]:
        return fail("Please complete demo OTP verification before signing in.", 403)
    token = create_access_token(identity=user["id"])
    return jsonify({"success": True, "access_token": token, "citizen": public_user(user)})

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.services.demo_store import reset_store


def setup_function():
    reset_store()


def test_health():
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/api/health").status_code == 200


def test_register_verify_and_profile():
    app = create_app({
        "TESTING": True,
        "APP_MODE": "demo",
        "JWT_SECRET_KEY": "verifyonce-test-secret-2026-long-random-key",
        "DEMO_OTP": "123456"
    })
    client = app.test_client()
    response = client.post("/api/auth/register", json={"full_name":"Sample Citizen", "email":"sample@example.test", "mobile":"9876543210", "password":"sample-pass-123"})
    assert response.status_code == 201
    verified = client.post("/api/auth/otp/verify", json={"identity":"sample@example.test", "otp":"123456"})
    assert verified.status_code == 200
    token = verified.get_json()["access_token"]
    profile = client.get("/api/citizens/me", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
    assert profile.get_json()["citizen"]["full_name"] == "Sample Citizen"

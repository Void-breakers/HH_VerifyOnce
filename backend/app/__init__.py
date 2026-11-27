from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from .config import Config
from .routes.auth import auth_bp
from .routes.citizen import citizen_bp


def create_app(test_config=None):
    root = Path(__file__).resolve().parents[2]
    frontend_dir = root / "frontend"
    app = Flask(__name__, static_folder=str(frontend_dir), static_url_path="")
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    JWTManager(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(citizen_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "healthy", "project": "VerifyOnce", "mode": app.config["APP_MODE"]})

    @app.get("/")
    def home():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/<path:filename>")
    def frontend_files(filename):
        return send_from_directory(frontend_dir, filename)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"success": False, "message": "Resource not found."}), 404

    return app

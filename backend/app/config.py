import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-only-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 4
    APP_MODE = os.getenv("APP_MODE", "demo")
    DEMO_OTP = os.getenv("DEMO_OTP", "123456")

"""Temporary in-memory repository for integration testing only.
Replace this adapter with the database teammate's Supabase/PostgreSQL schema.
Data is erased whenever the Flask process restarts.
"""
from uuid import uuid4

USERS_BY_EMAIL = {}
USERS_BY_MOBILE = {}
OTP_BY_USER = {}


def reset_store():
    USERS_BY_EMAIL.clear()
    USERS_BY_MOBILE.clear()
    OTP_BY_USER.clear()


def create_user(user):
    user["id"] = str(uuid4())
    USERS_BY_EMAIL[user["email"]] = user
    USERS_BY_MOBILE[user["mobile"]] = user
    return user


def find_user(identity):
    key = identity.strip().lower()
    return USERS_BY_EMAIL.get(key) or USERS_BY_MOBILE.get(identity.strip())

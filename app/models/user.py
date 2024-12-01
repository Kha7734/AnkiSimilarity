import hashlib
from datetime import datetime
# from app.databases.db import db  # Assuming you have a database connection set up
from flask import current_app

class User:
    def __init__(self, user_id, username, email, password_hash, created_at, last_login):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login

    @staticmethod
    def create_user(username, email, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(None, username, email, password_hash, datetime.now(), None)

        # Save to database
        current_app.db.users.insert_one(new_user.__dict__)
        return new_user

    @staticmethod
    def validate_user(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = current_app.db.users.find_one({"username": username})

        if user and user['password_hash'] == password_hash:
            return True  # Credentials are valid
        return False  # Invalid credentials

    @staticmethod
    def get_user_by_id(user_id):
        return current_app.db.users.find_one({"user_id": user_id})

    @staticmethod
    def update_user(user_id, update_fields):
        current_app.db.users.update_one({"user_id": user_id}, {"$set": update_fields})

    @staticmethod
    def delete_user(user_id):
        current_app.db.users.delete_one({"user_id": user_id})

    @staticmethod
    def set_last_login(user_id):
        current_app.db.users.update_one({"user_id": user_id}, {"$set": {"last_login": datetime.now()}})

    @staticmethod
    def check_username_exists(username):
        return current_app.db.users.find_one({"username": username}) is not None

    @staticmethod
    def check_email_exists(email):
        return current_app.db.users.find_one({"email": email}) is not None

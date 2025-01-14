# models/user.py
import hashlib
from datetime import datetime, timedelta
import jwt  # Import JWT library
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
        # Update user_id with the generated ObjectId and convert it to a string
        new_user.user_id = str(new_user._id)
        current_app.db.users.update_one({"_id": new_user._id}, {"$set": {"user_id": new_user.user_id}})

        return new_user

    @staticmethod
    def validate_user(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = current_app.db.users.find_one({"username": username})

        if user and user['password_hash'] == password_hash:
            return user  # Return the user document if credentials are valid
        return None  # Invalid credentials

    @staticmethod
    def generate_token(user_id, username):
        """
        Generate a JWT token for the user.
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        }
        # Use a secret key from Flask's configuration
        secret_key = current_app.config['SECRET_KEY']
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

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
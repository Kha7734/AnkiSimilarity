from functools import wraps
from flask import jsonify, redirect, url_for, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Verify JWT token
            user_id = get_jwt_identity()  # Get the user ID from the token
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": f"Unauthorized"}), 401
    return decorated_function
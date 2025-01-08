# routes/user_routes.py
from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from app.models.user import User
import hashlib

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.check_username_exists(data['username']):
        return jsonify({'message': 'Username already exists'}), 400
    if User.check_email_exists(data['email']):
        return jsonify({'message': 'Email already exists'}), 400

    user = User.create_user(data['username'], data['email'], data['password'])
    return jsonify({'message': 'User created successfully'}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.validate_user(data['username'], data['password'])
    if user:
        User.set_last_login(user['user_id'])

        # Generate a JWT token
        token = User.generate_token(user['user_id'], user['username'])

        user_data = {
            '_id': str(user['_id']),
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user.get('last_login')
        }

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'data': user_data
        }), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@user_bp.route('/validate-token', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 400

    try:
        # Decode the token using the secret key
        secret_key = current_app.config['SECRET_KEY']
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Fetch user data from the database
        user = User.get_user_by_id(payload['user_id'])
        if user:
            return jsonify({
                'message': 'Token is valid',
                'user_id': user['user_id'],
                'username': user['username']
            }), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@user_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        return jsonify({
            'user_id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user.get('last_login')
        }), 200
    return jsonify({'message': 'User not found'}), 404


@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    update_fields = {}

    if 'email' in data:
        update_fields['email'] = data['email']
    if 'password' in data:
        update_fields['password_hash'] = hashlib.sha256(data['password'].encode()).hexdigest()

    User.update_user(user_id, update_fields)
    return jsonify({'message': 'User updated successfully'}), 200


@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'}), 200
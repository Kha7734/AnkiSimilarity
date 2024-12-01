# routes/user_routes.py

from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
# from app.databases.db import db
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
    if User.validate_user(data['username'], data['password']):
        user = current_app.db.users.find_one({"username": data['username']})
        User.set_last_login(user['user_id'])
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401


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

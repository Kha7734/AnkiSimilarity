from flask import Blueprint, request, jsonify, current_app  # Import current_app
from bson import ObjectId
from app.utils.decorators import login_required

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['POST'])
@login_required
def create_settings():
    data = request.json
    user_id = data['user_id']
    language_preference = data.get('language_preference', 'en')
    daily_goal = data.get('daily_goal', 20)
    notification_enabled = data.get('notification_enabled', True)
    notification_time = data.get('notification_time', '09:00')
    theme = data.get('theme', 'light')

    settings = {
        "user_id": user_id,
        "language_preference": language_preference,
        "daily_goal": daily_goal,
        "notification_enabled": notification_enabled,
        "notification_time": notification_time,
        "theme": theme
    }
    result = current_app.db.settings.insert_one(settings)  # Use current_app
    return jsonify({'message': 'Settings created successfully', 'settings_id': str(result.inserted_id)}), 201

@settings_bp.route('/settings/<user_id>', methods=['GET'])
@login_required
def get_settings(user_id):
    settings = current_app.db.settings.find_one({"user_id": user_id})  # Use current_app
    if settings:
        return jsonify({
            'settings_id': str(settings['_id']),
            'user_id': str(settings['user_id']),
            'language_preference': settings['language_preference'],
            'daily_goal': settings['daily_goal'],
            'notification_enabled': settings['notification_enabled'],
            'notification_time': settings['notification_time'],
            'theme': settings['theme']
        }), 200
    return jsonify({'message': 'Settings not found'}), 404

@settings_bp.route('/settings/<user_id>', methods=['PUT'])
@login_required
def update_settings(user_id):
    data = request.json
    update_fields = {}

    if 'language_preference' in data:
        update_fields['language_preference'] = data['language_preference']
    if 'daily_goal' in data:
        update_fields['daily_goal'] = data['daily_goal']
    if 'notification_enabled' in data:
        update_fields['notification_enabled'] = data['notification_enabled']
    if 'notification_time' in data:
        update_fields['notification_time'] = data['notification_time']
    if 'theme' in data:
        update_fields['theme'] = data['theme']

    result = current_app.db.settings.update_one(  # Use current_app
        {"user_id": user_id},
        {"$set": update_fields}
    )
    if result.matched_count > 0:
        return jsonify({'message': 'Settings updated successfully'}), 200
    return jsonify({'message': 'Settings not found'}), 404

@settings_bp.route('/settings/<user_id>', methods=['DELETE'])
@login_required
def delete_settings(user_id):
    result = current_app.db.settings.delete_one({"user_id": user_id})  # Use current_app
    if result.deleted_count > 0:
        return jsonify({'message': 'Settings deleted successfully'}), 200
    return jsonify({'message': 'Settings not found'}), 404
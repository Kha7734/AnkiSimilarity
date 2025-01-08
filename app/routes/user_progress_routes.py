from flask import Blueprint, request, jsonify, current_app  # Import current_app
from bson import ObjectId
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/api/progress', methods=['POST'])
def create_progress():
    data = request.json
    user_id = data['user_id']
    card_id = data['card_id']
    dataset_id = data['dataset_id']
    status = data.get('status', 'new')

    progress = {
        "user_id": user_id,
        "card_id": card_id,
        "dataset_id": dataset_id,
        "status": status,
        "last_reviewed": None,
        "next_review": None,
        "streak": 0,
        "ease_factor": 2.5,
        "interval": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = current_app.db.user_progress.insert_one(progress)  # Use current_app instead of request.app
    return jsonify({'message': 'Progress created successfully', 'progress_id': str(result.inserted_id)}), 201

@progress_bp.route('/api/progress/<progress_id>', methods=['GET'])
def get_progress(progress_id):
    progress = current_app.db.user_progress.find_one({"_id": ObjectId(progress_id)})  # Use current_app
    if progress:
        return jsonify({
            'progress_id': str(progress['_id']),
            'user_id': str(progress['user_id']),
            'card_id': str(progress['card_id']),
            'dataset_id': str(progress['dataset_id']),
            'status': progress['status'],
            'last_reviewed': progress.get('last_reviewed'),
            'next_review': progress.get('next_review'),
            'streak': progress['streak'],
            'ease_factor': progress['ease_factor'],
            'interval': progress['interval'],
            'created_at': progress['created_at'],
            'updated_at': progress['updated_at']
        }), 200
    return jsonify({'message': 'Progress not found'}), 404

@progress_bp.route('/api/progress/<progress_id>', methods=['PUT'])
def update_progress(progress_id):
    data = request.json
    update_fields = {}

    if 'status' in data:
        update_fields['status'] = data['status']
    if 'last_reviewed' in data:
        update_fields['last_reviewed'] = datetime.utcnow()
    if 'next_review' in data:
        update_fields['next_review'] = data['next_review']
    if 'streak' in data:
        update_fields['streak'] = data['streak']
    if 'ease_factor' in data:
        update_fields['ease_factor'] = data['ease_factor']
    if 'interval' in data:
        update_fields['interval'] = data['interval']
    update_fields['updated_at'] = datetime.utcnow()

    result = current_app.db.user_progress.update_one(  # Use current_app
        {"_id": ObjectId(progress_id)},
        {"$set": update_fields}
    )
    if result.matched_count > 0:
        return jsonify({'message': 'Progress updated successfully'}), 200
    return jsonify({'message': 'Progress not found'}), 404

@progress_bp.route('/api/progress/<progress_id>', methods=['DELETE'])
def delete_progress(progress_id):
    result = current_app.db.user_progress.delete_one({"_id": ObjectId(progress_id)})  # Use current_app
    if result.deleted_count > 0:
        return jsonify({'message': 'Progress deleted successfully'}), 200
    return jsonify({'message': 'Progress not found'}), 404

@progress_bp.route('/api/progress/user/<user_id>', methods=['GET'])
def get_progress_by_user(user_id):
    progress_entries = current_app.db.user_progress.find({"user_id": user_id})  # Fetch all progress entries for the user
    progress_list = []
    for progress in progress_entries:
        progress_list.append({
            'progress_id': str(progress['_id']),
            'user_id': str(progress['user_id']),
            'card_id': str(progress['card_id']),
            'dataset_id': str(progress['dataset_id']),
            'status': progress['status'],
            'last_reviewed': progress.get('last_reviewed'),
            'next_review': progress.get('next_review'),
            'streak': progress['streak'],
            'ease_factor': progress['ease_factor'],
            'interval': progress['interval'],
            'created_at': progress['created_at'],
            'updated_at': progress['updated_at']
        })
    return jsonify(progress_list), 200
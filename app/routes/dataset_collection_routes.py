from flask import Blueprint, request, jsonify, current_app  # Import current_app
from bson import ObjectId
from datetime import datetime

dataset_bp = Blueprint('dataset', __name__)

@dataset_bp.route('/datasets', methods=['POST'])
def create_dataset():
    data = request.json
    user_id = data['user_id']
    name = data['name']
    description = data.get('description', '')

    # Check if the dataset name already exists for the user
    if current_app.db.datasets.find_one({"user_id": user_id, "name": name}):  # Use current_app
        return jsonify({'message': 'Dataset name already exists for this user'}), 400

    dataset = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = current_app.db.datasets.insert_one(dataset)  # Use current_app
    return jsonify({'message': 'Dataset created successfully', 'dataset_id': str(result.inserted_id)}), 201

@dataset_bp.route('/datasets/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    dataset = current_app.db.datasets.find_one({"_id": ObjectId(dataset_id)})  # Use current_app
    if dataset:
        return jsonify({
            'dataset_id': str(dataset['_id']),
            'user_id': str(dataset['user_id']),
            'name': dataset['name'],
            'description': dataset['description'],
            'created_at': dataset['created_at'],
            'updated_at': dataset['updated_at']
        }), 200
    return jsonify({'message': 'Dataset not found'}), 404

@dataset_bp.route('/datasets/<dataset_id>', methods=['PUT'])
def update_dataset(dataset_id):
    data = request.json
    update_fields = {}

    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    update_fields['updated_at'] = datetime.utcnow()

    result = current_app.db.datasets.update_one(  # Use current_app
        {"_id": ObjectId(dataset_id)},
        {"$set": update_fields}
    )
    if result.matched_count > 0:
        return jsonify({'message': 'Dataset updated successfully'}), 200
    return jsonify({'message': 'Dataset not found'}), 404

@dataset_bp.route('/datasets/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    result = current_app.db.datasets.delete_one({"_id": ObjectId(dataset_id)})  # Use current_app
    if result.deleted_count > 0:
        return jsonify({'message': 'Dataset deleted successfully'}), 200
    return jsonify({'message': 'Dataset not found'}), 404
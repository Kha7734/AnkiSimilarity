from flask import Blueprint, request, jsonify
from flask import current_app
from app.models.card_collection import VocabularyCard  # Import the VocabularyCard model
from bson import json_util

# Create a Blueprint for vocabulary cards
vocab_bp = Blueprint('vocab', __name__)

@vocab_bp.route('/cards', methods=['POST'])
def create_card():
    data = request.json
    new_card = VocabularyCard.create_card(
        user_id=data['user_id'],
        dataset_id=data['dataset_id'],
        word=data['word'],
        meaning_en=data['meaning_en'],
        meaning_vi=data['meaning_vi'],
        ipa_transcription=data.get('ipa_transcription', ''),
        example_sentences_en=data.get('example_sentences_en', []),
        example_sentences_vi=data.get('example_sentences_vi', []),
        visual_image_url=data.get('visual_image_url', ''),
        audio_url_en=data.get('audio_url_en', ''),
        audio_url_vi=data.get('audio_url_vi', '')
    )

    # Return the created card's details, including its ID
    return json_util.dumps(new_card.__dict__), 201
@vocab_bp.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    card = VocabularyCard.get_card_by_id(card_id)
    if card:
        return json_util.dumps(card), 200
    return jsonify({"error": "Card not found"}), 404


@vocab_bp.route('/cards/<card_id>', methods=['PUT'])
def update_card(card_id):
    # Check if the card exists
    existing_card = current_app.db.vocabulary_cards.find_one({"card_id": card_id})

    if not existing_card:
        return jsonify({"error": "Card not found"}), 404  # Return 404 if card does not exist

    data = request.json

    # Prepare fields to update, excluding user_id if present
    update_fields = {k: v for k, v in data.items() if k != 'user_id'}

    # Update the card in the database
    result = current_app.db.vocabulary_cards.update_one({"card_id": card_id}, {"$set": update_fields})

    if result.modified_count == 0:
        return jsonify({"error": "No changes made to the card"}), 400  # Return 400 if no changes were made

    return jsonify({"message": "Card updated successfully"}), 200


@vocab_bp.route('/cards/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    VocabularyCard.delete_card(card_id)
    return jsonify({"message": "Card deleted successfully"}), 204

@vocab_bp.route('/users/<user_id>/cards', methods=['GET'])
def get_user_cards(user_id):
    cards = VocabularyCard.get_cards_by_user(user_id)
    return jsonify(cards), 200

@vocab_bp.route('/datasets/<dataset_id>/cards', methods=['GET'])
def get_dataset_cards(dataset_id):
    cards = VocabularyCard.get_cards_by_dataset(dataset_id)
    return jsonify(cards), 200

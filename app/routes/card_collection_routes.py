from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required
from flask import current_app
from app.models.card_collection import VocabularyCard  # Import the VocabularyCard model
from bson import json_util
import base64
from io import BytesIO
from gtts import gTTS

# Create a Blueprint for vocabulary cards
vocab_bp = Blueprint('vocab', __name__)

@vocab_bp.route('/cards', methods=['POST'])
@login_required
def create_card():
    data = request.json

    # Validate required fields
    if not data.get('user_id') or not data.get('dataset_id') or not data.get('word'):
        return jsonify({"error": "Missing required fields: user_id, dataset_id, or word"}), 400

    try:
        # Create the new vocabulary card
        new_card = VocabularyCard.create_card(
            user_id=data['user_id'],
            dataset_id=data['dataset_id'],
            word=data['word'],
            meaning_en=data.get('meaning_en'),  # Optional field
            meaning_vi=data.get('meaning_vi'),  # Optional field
            ipa_transcription=data.get('ipa_transcription'),  # Optional field
            example_sentences_en=data.get('example_sentences_en', []),  # Optional field
            example_sentences_vi=data.get('example_sentences_vi', []),  # Optional field
            visual_image_url=data.get('visual_image_url', ''),  # Optional field
            word_type=data.get('word_type'),  # Optional field
            vocab_family=data.get('vocab_family', [])  # Optional field
        )

        if not new_card:
            return jsonify({"error": "Failed to create vocabulary card"}), 500

        # Return the created card's details, including its ID
        return jsonify({
            "card_id": new_card.card_id,
            "user_id": new_card.user_id,
            "dataset_id": new_card.dataset_id,
            "word": new_card.word,
            "meaning_en": new_card.meaning_en,
            "meaning_vi": new_card.meaning_vi,
            "ipa_transcription": new_card.ipa_transcription,
            "example_sentences_en": new_card.example_sentences_en,
            "example_sentences_vi": new_card.example_sentences_vi,
            "visual_image_url": new_card.visual_image_url,
            "audio_url_word": new_card.audio_url_word,
            "audio_url_example1": new_card.audio_url_example1,
            "audio_url_example2": new_card.audio_url_example2,
            "synonyms": new_card.synonyms,
            "antonyms": new_card.antonyms,
            "word_type": new_card.word_type,
            "vocab_family": new_card.vocab_family,
            "created_at": new_card.created_at,
            "updated_at": new_card.updated_at
        }), 201

    except Exception as e:
        print(f"Error creating vocabulary card: {e}")
        return jsonify({"error": "An error occurred while creating the vocabulary card"}), 500

@vocab_bp.route('/cards/<card_id>', methods=['GET'])
@login_required
def get_card(card_id):
    card = VocabularyCard.get_card_by_id(card_id)
    if card:
        return json_util.dumps(card), 200
    return jsonify({"error": "Card not found"}), 404

@vocab_bp.route('/cards/<card_id>', methods=['PUT'])
@login_required
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
@login_required
def delete_card(card_id):
    VocabularyCard.delete_card(card_id)
    return jsonify({"message": "Card deleted successfully"}), 204

@vocab_bp.route('/users/<user_id>/cards', methods=['GET'])
@login_required
def get_user_cards(user_id):
    cards = VocabularyCard.get_cards_by_user(user_id)
    return jsonify(cards), 200

@vocab_bp.route('/datasets/<dataset_id>/cards', methods=['GET'])
@login_required
def get_dataset_cards(dataset_id):
    cards = VocabularyCard.get_cards_by_dataset(dataset_id)
    return jsonify(cards), 200

@vocab_bp.route('/cards/generate', methods=['POST'])
@login_required
def generate_fields():
    data = request.json
    word = data.get('word')

    if not word:
        return jsonify({"error": "Word is required"}), 400

    # Generate IPA transcription
    ipa_transcription = VocabularyCard.get_ipa_transcription(word)

    # Generate synonyms and antonyms
    synonyms, antonyms = VocabularyCard.get_synonyms_antonyms(word)

    # Generate example sentences
    example_sentences_en = VocabularyCard.get_example_sentences(word)

    # Generate English meaning
    meaning_en = VocabularyCard.get_meaning_en(word)

    # Generate Vietnamese meaning
    meaning_vi = VocabularyCard.get_meaning_vi(word)

    # Generate word type
    word_type = VocabularyCard.get_word_type(word)

    # Generate vocabulary family
    vocab_family = VocabularyCard.get_vocab_family(word)

    # Generate audio for the word
    tts = gTTS(text=word, lang='en')
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    # Convert audio to base64
    audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

    # Return the generated fields
    return jsonify({
        "ipa_transcription": ipa_transcription,
        "synonyms": synonyms,
        "antonyms": antonyms,
        "example_sentences_en": example_sentences_en,
        "meaning_en": meaning_en,
        "meaning_vi": meaning_vi,
        "word_type": word_type,  # New field: word type
        "vocab_family": vocab_family,  # New field: vocabulary family
        "audio_base64": audio_base64  # New field: base64-encoded audio
    }), 200
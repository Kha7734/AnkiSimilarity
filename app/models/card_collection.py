# models/card_collection.py
import datetime
from flask import current_app

class VocabularyCard:
    def __init__(self, card_id, user_id, dataset_id, word, meaning_en, meaning_vi,
                 ipa_transcription, example_sentences_en, example_sentences_vi,
                 visual_image_url, audio_url_en, audio_url_vi,
                 created_at=None, updated_at=None):
        self.card_id = card_id
        self.user_id = user_id
        self.dataset_id = dataset_id
        self.word = word
        self.meaning_en = meaning_en
        self.meaning_vi = meaning_vi
        self.ipa_transcription = ipa_transcription
        self.example_sentences_en = example_sentences_en
        self.example_sentences_vi = example_sentences_vi
        self.visual_image_url = visual_image_url
        self.audio_url_en = audio_url_en
        self.audio_url_vi = audio_url_vi
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.updated_at = updated_at if updated_at else datetime.datetime.now()

    @staticmethod
    def create_card(user_id, dataset_id, word, meaning_en, meaning_vi,
                    ipa_transcription, example_sentences_en, example_sentences_vi,
                    visual_image_url, audio_url_en, audio_url_vi):
        new_card = VocabularyCard(
            None,
            user_id,
            dataset_id,
            word,
            meaning_en,
            meaning_vi,
            ipa_transcription,
            example_sentences_en,
            example_sentences_vi,
            visual_image_url,
            audio_url_en,
            audio_url_vi
        )

        # Save to database (assuming a MongoDB-like structure)
        result = current_app.db.vocabulary_cards.insert_one(new_card.__dict__)

        # Update the card_id with the generated ID
        new_card.card_id = str(result.inserted_id)

        # Update the card in the database with the new card_id
        current_app.db.vocabulary_cards.update_one({"_id": result.inserted_id},
                                                   {"$set": {"card_id": new_card.card_id}})

        return new_card

    @staticmethod
    def get_card_by_id(card_id):
        return current_app.db.vocabulary_cards.find_one({"card_id": card_id})

    @staticmethod
    def update_card(card_id, update_fields):
        update_fields['updated_at'] = datetime.datetime.now()  # Update timestamp on modification
        current_app.db.vocabulary_cards.update_one({"card_id": card_id}, {"$set": update_fields})

    @staticmethod
    def delete_card(card_id):
        current_app.db.vocabulary_cards.delete_one({"card_id": card_id})

    @staticmethod
    def get_cards_by_user(user_id):
        return list(current_app.db.vocabulary_cards.find({"user_id": user_id}))

    @staticmethod
    def get_cards_by_dataset(dataset_id):
        return list(current_app.db.vocabulary_cards.find({"dataset_id": dataset_id}))

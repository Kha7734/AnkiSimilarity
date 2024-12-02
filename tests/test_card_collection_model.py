# # tests/test_card_collection_model.py
#
# import unittest
# from app import create_app
# # from app.models.card_collection import VocabularyCard  # Import your VocabularyCard model
# # from app.databases.db import db  # Ensure you have access to your database connection
# from flask import current_app
#
# class TestVocabularyCardModel(unittest.TestCase):
#
#     def setUp(self):
#         self.app = create_app()
#         self.app_context = self.app.app_context()  # Create an application context
#         self.app_context.push()  # Push the application context
#
#         # Set up a test vocabulary card in the database before each test
#         self.test_card_data = {
#             "user_id": "test_user_id",
#             "dataset_id": "test_dataset_id",
#             "word": "testword",
#             "meaning_en": "a test word",
#             "meaning_vi": "một từ thử nghiệm",
#             "ipa_transcription": "/tɛstwɜrd/",
#             "example_sentences_en": ["This is a test sentence.", "Another example of a test."],
#             "example_sentences_vi": ["Đây là một câu thử nghiệm.", "Một ví dụ khác về thử nghiệm."],
#             "visual_image_url": "http://example.com/image.jpg",
#             "audio_url_en": "http://example.com/audio_en.mp3",
#             "audio_url_vi": "http://example.com/audio_vi.mp3"
#         }
#
#         # Create the test card and store its ID for later use
#         self.card = VocabularyCard.create_card(**self.test_card_data)
#
#     def tearDown(self):
#         # Clean up after each test by deleting the test card using its card ID
#         VocabularyCard.delete_card(self.card.card_id)  # Use the card ID of the created card
#         self.app_context.pop()  # Pop the application context
#
#     def test_create_card(self):
#         card = VocabularyCard.get_card_by_id({"card_id": self.card.card_id})
#         self.assertIsNotNone(card)
#         self.assertEqual(card['meaning_en'], self.test_card_data['meaning_en'])
#
#     def test_update_card(self):
#         update_data = {"meaning_en": "updated meaning"}
#         db.vocabulary_cards.update_card(self.card.card_id, update_data)
#
#         updated_card = VocabularyCard.get_card_by_id(self.card.card_id)
#         self.assertEqual(updated_card['meaning_en'], update_data['meaning_en'])
#
#     def test_delete_card(self):
#         VocabularyCard.delete_card(self.card.card_id)
#         # deleted_card = db.vocabulary_cards.find_one({"word": self.test_card_data["word"]})
#         deleted_card = VocabularyCard.get_card_by_id(self.card.card_id)
#         self.assertIsNone(deleted_card)
#
#
# if __name__ == '__main__':
#     unittest.main()

import unittest
from flask import json, current_app
from app import create_app
from app.models.card_collection import VocabularyCard  # Import your VocabularyCard model



class TestVocabularyCardModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the application context
        self.client = self.app.test_client()  # Create a test client

        # Set up a test vocabulary card in the database before each test
        self.test_card_data = {
            "user_id": "test_user_id",
            "dataset_id": "test_dataset_id",
            "word": "testword",
            "meaning_en": "a test word",
            "meaning_vi": "một từ thử nghiệm",
            "ipa_transcription": "/tɛstwɜrd/",
            "example_sentences_en": ["This is a test sentence.", "Another example of a test."],
            "example_sentences_vi": ["Đây là một câu thử nghiệm.", "Một ví dụ khác về thử nghiệm."],
            "visual_image_url": "http://example.com/image.jpg",
            "audio_url_en": "http://example.com/audio_en.mp3",
            "audio_url_vi": "http://example.com/audio_vi.mp3"
        }

        # Create the test card and store its ID for later use
        self.card = VocabularyCard.create_card(**self.test_card_data)

    def tearDown(self):
        # Clean up after each test by deleting the test card using its card ID
        VocabularyCard.delete_card(self.card.card_id)  # Use the card ID of the created card
        self.app_context.pop()  # Pop the application context

    def test_create_card(self):
        card = current_app.db.vocabulary_cards.find_one({"word": self.test_card_data["word"]})
        self.assertIsNotNone(card)
        self.assertEqual(card['meaning_en'], self.test_card_data['meaning_en'])

    def test_update_card(self):
        update_data = {"meaning_en": "updated meaning"}

        # Update the card using its ID from setup
        response = self.client.put(f'/cards/{self.card.card_id}', json=update_data)

        # Ensure the update request was successful
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Retrieve the updated card
        updated_card = current_app.db.vocabulary_cards.find_one({"card_id": self.card.card_id})

        # Check if updated_card is not None before accessing its fields
        self.assertIsNotNone(updated_card, msg="Updated card should not be None after update.")

        # Now check if the meaning was updated correctly
        self.assertEqual(updated_card['meaning_en'], update_data['meaning_en'],
                         msg=f"Expected meaning_en to be '{update_data['meaning_en']}' but got '{updated_card['meaning_en']}'")

    def test_delete_card(self):
        VocabularyCard.delete_card(self.card.card_id)

        deleted_card = current_app.db.vocabulary_cards.find_one({"card_id": self.card.card_id})
        self.assertIsNone(deleted_card)


if __name__ == '__main__':
    unittest.main()

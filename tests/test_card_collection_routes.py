# tests/test_card_collection_routes.py

import unittest
from flask import json, current_app
from app import create_app
from app.databases.db import db  # Ensure you have access to your database connection

class TestVocabularyCardRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test client
        self.client = self.app.test_client()

        # Set up a test vocabulary card in the database before each test
        self.test_card_data = {
            "user_id": "test_user_id",
            "dataset_id": "test_dataset_id",
            "word": "testword",
            "meaning_en": "a test word",
            "meaning_vi": "một từ thử nghiệm",
            "ipa_transcription": "/tɛstwɜrd/",
            "example_sentences_en": ["This is a test sentence."],
            "example_sentences_vi": ["Đây là một câu thử nghiệm."],
            "visual_image_url": "http://example.com/image.jpg",
            "audio_url_en": "http://example.com/audio_en.mp3",
            "audio_url_vi": "http://example.com/audio_vi.mp3"
        }

        # Create the test card and store its ID for later use
        response = self.client.post('/cards', json=self.test_card_data)
        # Get the card ID from the response data
        self.card_id = json.loads(response.data)['card_id']

    def tearDown(self):
        # Clean up after each test by deleting any vocabulary cards created during tests
        db.vocabulary_cards.delete_one({"card_id": self.card_id})

    def test_create_card(self):
        response = self.client.post('/cards', json=self.test_card_data)
        self.assertEqual(response.status_code, 201)

    def test_get_card(self):
        # Retrieve the card using its ID from setup
        response = self.client.get(f'/cards/{self.card_id}')  # Use the saved card ID
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Optionally check if the returned data matches expected data
        data = json.loads(response.data)
        self.assertEqual(data['word'], self.test_card_data['word'])
        self.assertEqual(data['meaning_en'], self.test_card_data['meaning_en'])

    def test_update_card(self):
        update_data = {"meaning_en": "updated meaning"}

        # Update the card using its ID from setup
        response = self.client.put(f'/cards/{self.card_id}', json=update_data)

        # Ensure the update request was successful
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Retrieve the updated card
        updated_card = current_app.db.vocabulary_cards.find_one({"card_id": self.card_id})

        # Check if updated_card is not None before accessing its fields
        self.assertIsNotNone(updated_card, msg="Updated card should not be None after update.")

        # Now check if the meaning was updated correctly
        self.assertEqual(updated_card['meaning_en'], update_data['meaning_en'],
                         msg=f"Expected meaning_en to be '{update_data['meaning_en']}' but got '{updated_card['meaning_en']}'")

    def test_delete_card(self):
        # Delete the card using its ID from setup
        response = self.client.delete(f'/cards/{self.card_id}')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()

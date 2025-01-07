import unittest
from datetime import datetime
from bson import ObjectId

from app.databases.db import close_db
from app.models.card_collection import VocabularyCard
from app import create_app

class TestVocabularyCardModel(unittest.TestCase):
    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Initialize the test database
        self.test_db = self.app.db

        # Clear collections in the test database
        self.test_db.vocabulary_cards.delete_many({})

        # Initialize test data
        self.user_id = ObjectId()
        self.dataset_id = ObjectId()

    def tearDown(self):
        # Clear collections in the test database
        self.test_db.vocabulary_cards.delete_many({})

        close_db()

        # Pop the app context
        self.app_context.pop()

    def test_create_card(self):
        # Create a new vocabulary card
        card = VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )

        # Check if the card was created successfully
        self.assertIsNotNone(card.card_id)
        self.assertEqual(card.user_id, self.user_id)
        self.assertEqual(card.dataset_id, self.dataset_id)
        self.assertEqual(card.word, "apple")
        self.assertEqual(card.meaning_en, "A fruit")
        self.assertEqual(card.meaning_vi, "Một loại trái cây")
        self.assertEqual(card.ipa_transcription, "/ˈæp.əl/")
        self.assertEqual(card.example_sentences_en, ["I ate an apple."])
        self.assertEqual(card.example_sentences_vi, ["Tôi đã ăn một quả táo."])
        self.assertEqual(card.visual_image_url, "http://example.com/apple.jpg")
        self.assertEqual(card.audio_url_en, "http://example.com/apple_en.mp3")
        self.assertEqual(card.audio_url_vi, "http://example.com/apple_vi.mp3")
        self.assertIsInstance(card.created_at, datetime)
        self.assertIsInstance(card.updated_at, datetime)

    def test_get_card_by_id(self):
        # Create a card first
        card = VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )

        # Retrieve the card by ID
        retrieved_card = VocabularyCard.get_card_by_id(card.card_id)
        self.assertIsNotNone(retrieved_card)
        self.assertEqual(retrieved_card['word'], "apple")

    def test_update_card(self):
        # Create a card first
        card = VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )

        # Update the card
        update_fields = {
            "word": "banana",
            "meaning_en": "Another fruit",
            "meaning_vi": "Một loại trái cây khác"
        }
        VocabularyCard.update_card(card.card_id, update_fields)

        # Retrieve the updated card
        updated_card = VocabularyCard.get_card_by_id(card.card_id)
        self.assertEqual(updated_card['word'], "banana")
        self.assertEqual(updated_card['meaning_en'], "Another fruit")
        self.assertEqual(updated_card['meaning_vi'], "Một loại trái cây khác")

    def test_delete_card(self):
        # Create a card first
        card = VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )

        # Delete the card
        VocabularyCard.delete_card(card.card_id)

        # Verify the card is deleted
        deleted_card = VocabularyCard.get_card_by_id(card.card_id)
        self.assertIsNone(deleted_card)

    def test_get_cards_by_user(self):
        # Create two cards for the same user
        VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )
        VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="banana",
            meaning_en="Another fruit",
            meaning_vi="Một loại trái cây khác",
            ipa_transcription="/bəˈnɑː.nə/",
            example_sentences_en=["I like bananas."],
            example_sentences_vi=["Tôi thích chuối."],
            visual_image_url="http://example.com/banana.jpg",
            audio_url_en="http://example.com/banana_en.mp3",
            audio_url_vi="http://example.com/banana_vi.mp3"
        )

        # Retrieve cards by user ID
        cards = VocabularyCard.get_cards_by_user(self.user_id)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]['word'], "apple")
        self.assertEqual(cards[1]['word'], "banana")

    def test_get_cards_by_dataset(self):
        # Create two cards for the same dataset
        VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="apple",
            meaning_en="A fruit",
            meaning_vi="Một loại trái cây",
            ipa_transcription="/ˈæp.əl/",
            example_sentences_en=["I ate an apple."],
            example_sentences_vi=["Tôi đã ăn một quả táo."],
            visual_image_url="http://example.com/apple.jpg",
            audio_url_en="http://example.com/apple_en.mp3",
            audio_url_vi="http://example.com/apple_vi.mp3"
        )
        VocabularyCard.create_card(
            user_id=self.user_id,
            dataset_id=self.dataset_id,
            word="banana",
            meaning_en="Another fruit",
            meaning_vi="Một loại trái cây khác",
            ipa_transcription="/bəˈnɑː.nə/",
            example_sentences_en=["I like bananas."],
            example_sentences_vi=["Tôi thích chuối."],
            visual_image_url="http://example.com/banana.jpg",
            audio_url_en="http://example.com/banana_en.mp3",
            audio_url_vi="http://example.com/banana_vi.mp3"
        )

        # Retrieve cards by dataset ID
        cards = VocabularyCard.get_cards_by_dataset(self.dataset_id)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]['word'], "apple")
        self.assertEqual(cards[1]['word'], "banana")

if __name__ == '__main__':
    unittest.main()
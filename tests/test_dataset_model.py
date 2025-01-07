import unittest
from datetime import datetime
from bson import ObjectId
from app.models.dataset_collection import Dataset
from app import create_app

class TestDatasetModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.test_db = self.app.db

        # Clear collections in the test database
        self.test_db.vocabulary_cards.delete_many({})
        self.test_db.datasets.delete_many({})
        self.test_db.user_progress.delete_many({})
        self.test_db.settings.delete_many({})

        self.user_id = ObjectId()

    def tearDown(self):
        # Clear collections in the test database
        self.test_db.vocabulary_cards.delete_many({})
        self.test_db.datasets.delete_many({})
        self.test_db.user_progress.delete_many({})
        self.test_db.settings.delete_many({})

        self.app_context.pop()

    def test_create_dataset(self):
        dataset = Dataset(
            user_id=self.user_id,
            name="Test Dataset",
            description="This is a test dataset"
        )
        dataset_dict = dataset.to_dict()
        self.assertIn('_id', dataset_dict)
        self.assertEqual(dataset_dict['user_id'], self.user_id)
        self.assertEqual(dataset_dict['name'], "Test Dataset")
        self.assertEqual(dataset_dict['description'], "This is a test dataset")
        self.assertIsInstance(dataset_dict['created_at'], datetime)
        self.assertIsInstance(dataset_dict['updated_at'], datetime)

    def test_save_dataset(self):
        dataset = Dataset(
            user_id=self.user_id,
            name="Test Dataset",
            description="This is a test dataset"
        )
        dataset_id = self.test_db.datasets.insert_one(dataset.to_dict()).inserted_id
        saved_dataset = self.test_db.datasets.find_one({"_id": dataset_id})
        self.assertIsNotNone(saved_dataset)
        self.assertEqual(saved_dataset['name'], "Test Dataset")

if __name__ == '__main__':
    unittest.main()
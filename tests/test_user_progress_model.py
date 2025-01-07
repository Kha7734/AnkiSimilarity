import unittest
from datetime import datetime
from bson import ObjectId
from app.models.user_progress import UserProgress
from app import create_app, close_db

class TestUserProgressModel(unittest.TestCase):
    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Initialize the test database and store the client for cleanup
        self.test_db = self.app.db  # Assuming init_test_db returns (client, db)

        # Clear collections in the test database
        self.test_db.user_progress.delete_many({})

        # Initialize test data
        self.user_id = ObjectId()
        self.card_id = ObjectId()
        self.dataset_id = ObjectId()

    def tearDown(self):
        # Clear collections in the test database
        self.test_db.user_progress.delete_many({})

        # Close the database connection
        close_db()

        # Pop the app context
        self.app_context.pop()

    def test_create_user_progress(self):
        # Create a UserProgress instance
        progress = UserProgress(
            user_id=self.user_id,
            card_id=self.card_id,
            dataset_id=self.dataset_id,
            status="learning"
        )
        progress_dict = progress.to_dict()

        # Assert that the progress object is created correctly
        self.assertIn('_id', progress_dict)
        self.assertEqual(progress_dict['user_id'], self.user_id)
        self.assertEqual(progress_dict['card_id'], self.card_id)
        self.assertEqual(progress_dict['dataset_id'], self.dataset_id)
        self.assertEqual(progress_dict['status'], "learning")
        self.assertEqual(progress_dict['streak'], 0)
        self.assertEqual(progress_dict['ease_factor'], 2.5)
        self.assertEqual(progress_dict['interval'], 1)

    def test_save_user_progress(self):
        # Create a UserProgress instance
        progress = UserProgress(
            user_id=self.user_id,
            card_id=self.card_id,
            dataset_id=self.dataset_id,
            status="learning"
        )

        # Save the progress to the test database
        progress_id = self.test_db.user_progress.insert_one(progress.to_dict()).inserted_id

        # Retrieve the saved progress from the database
        saved_progress = self.test_db.user_progress.find_one({"_id": progress_id})

        # Assert that the progress was saved correctly
        self.assertIsNotNone(saved_progress)
        self.assertEqual(saved_progress['status'], "learning")
        self.assertEqual(saved_progress['user_id'], self.user_id)
        self.assertEqual(saved_progress['card_id'], self.card_id)
        self.assertEqual(saved_progress['dataset_id'], self.dataset_id)

if __name__ == '__main__':
    unittest.main()
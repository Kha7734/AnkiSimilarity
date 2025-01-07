import unittest
from flask import json
from bson import ObjectId
from datetime import datetime
from app import create_app

class TestUserProgressRoutes(unittest.TestCase):

    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test client
        self.client = self.app.test_client()

        # Clear the user_progress collection in the test database
        self.app.db.user_progress.delete_many({})

        # Set up test data
        self.user_id = str(ObjectId())
        self.card_id = str(ObjectId())
        self.dataset_id = str(ObjectId())

        # Create a test progress record
        self.test_progress_data = {
            "user_id": self.user_id,
            "card_id": self.card_id,
            "dataset_id": self.dataset_id,
            "status": "new"
        }

        # Insert the test progress record into the database
        response = self.client.post('/api/progress', json=self.test_progress_data)
        self.assertEqual(response.status_code, 201, msg=f"Failed to create test progress. Response: {response.data.decode()}")

        # Get the progress ID from the response data
        self.progress_id = json.loads(response.data)['progress_id']

    def tearDown(self):
        # Clean up after each test by deleting any progress records created during tests
        self.app.db.user_progress.delete_many({})

        # Pop the app context
        self.app_context.pop()

    def test_create_progress(self):
        # Test creating a new progress record
        new_progress_data = {
            "user_id": str(ObjectId()),
            "card_id": str(ObjectId()),
            "dataset_id": str(ObjectId()),
            "status": "learning"
        }
        response = self.client.post('/api/progress', json=new_progress_data)
        self.assertEqual(response.status_code, 201)

        # Verify the progress record was created
        progress_id = json.loads(response.data)['progress_id']
        progress = self.app.db.user_progress.find_one({"_id": ObjectId(progress_id)})
        self.assertIsNotNone(progress)
        self.assertEqual(progress['status'], "learning")

    def test_get_progress(self):
        # Retrieve the progress record using its ID from setup
        response = self.client.get(f'/api/progress/{self.progress_id}')
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Verify the returned data matches the test data
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], self.user_id)
        self.assertEqual(data['card_id'], self.card_id)
        self.assertEqual(data['dataset_id'], self.dataset_id)
        self.assertEqual(data['status'], "new")

    def test_update_progress(self):
        # Update the progress record using its ID from setup
        update_data = {
            "status": "review",
            "streak": 1,
            "ease_factor": 2.6,
            "interval": 2
        }
        response = self.client.put(f'/api/progress/{self.progress_id}', json=update_data)

        # Ensure the update request was successful
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Retrieve the updated progress record
        updated_progress = self.app.db.user_progress.find_one({"_id": ObjectId(self.progress_id)})

        # Verify the fields were updated correctly
        self.assertEqual(updated_progress['status'], "review")
        self.assertEqual(updated_progress['streak'], 1)
        self.assertEqual(updated_progress['ease_factor'], 2.6)
        self.assertEqual(updated_progress['interval'], 2)

    def test_delete_progress(self):
        # Delete the progress record using its ID from setup
        response = self.client.delete(f'/api/progress/{self.progress_id}')
        self.assertEqual(response.status_code, 200)

        # Verify the progress record was deleted
        deleted_progress = self.app.db.user_progress.find_one({"_id": ObjectId(self.progress_id)})
        self.assertIsNone(deleted_progress)

if __name__ == '__main__':
    unittest.main()
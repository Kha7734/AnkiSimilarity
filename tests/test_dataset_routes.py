import unittest
from flask import json
from bson import ObjectId
from datetime import datetime
from app import create_app

class TestDatasetCollectionRoutes(unittest.TestCase):

    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test client
        self.client = self.app.test_client()

        # Clear the datasets collection in the test database
        self.app.db.datasets.delete_many({})

        # Set up test data
        self.user_id = str(ObjectId())
        self.dataset_name = "Test Dataset"
        self.dataset_description = "This is a test dataset."

        # Create a test dataset
        self.test_dataset_data = {
            "user_id": self.user_id,
            "name": self.dataset_name,
            "description": self.dataset_description
        }

        # Insert the test dataset into the database
        response = self.client.post('/datasets', json=self.test_dataset_data)
        self.assertEqual(response.status_code, 201, msg=f"Failed to create test dataset. Response: {response.data.decode()}")

        # Get the dataset ID from the response data
        self.dataset_id = json.loads(response.data)['dataset_id']

    def tearDown(self):
        # Clean up after each test by deleting any datasets created during tests
        self.app.db.datasets.delete_many({})

        # Pop the app context
        self.app_context.pop()

    def test_create_dataset(self):
        # Test creating a new dataset
        new_dataset_data = {
            "user_id": str(ObjectId()),
            "name": "New Dataset",
            "description": "This is a new dataset."
        }
        response = self.client.post('/datasets', json=new_dataset_data)
        self.assertEqual(response.status_code, 201)

        # Verify the dataset was created
        dataset_id = json.loads(response.data)['dataset_id']
        dataset = self.app.db.datasets.find_one({"_id": ObjectId(dataset_id)})
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset['name'], "New Dataset")

    def test_create_dataset_duplicate_name(self):
        # Test creating a dataset with a duplicate name for the same user
        duplicate_dataset_data = {
            "user_id": self.user_id,
            "name": self.dataset_name,
            "description": "This is a duplicate dataset."
        }
        response = self.client.post('/datasets', json=duplicate_dataset_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Dataset name already exists for this user", response.data.decode())

    def test_get_dataset(self):
        # Retrieve the dataset using its ID from setup
        response = self.client.get(f'/datasets/{self.dataset_id}')
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Verify the returned data matches the test data
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], self.user_id)
        self.assertEqual(data['name'], self.dataset_name)
        self.assertEqual(data['description'], self.dataset_description)

    def test_get_dataset_not_found(self):
        # Test retrieving a non-existent dataset
        non_existent_dataset_id = str(ObjectId())
        response = self.client.get(f'/datasets/{non_existent_dataset_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dataset not found", response.data.decode())

    def test_update_dataset(self):
        # Update the dataset using its ID from setup
        update_data = {
            "name": "Updated Dataset Name",
            "description": "This is an updated description."
        }
        response = self.client.put(f'/datasets/{self.dataset_id}', json=update_data)

        # Ensure the update request was successful
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Retrieve the updated dataset
        updated_dataset = self.app.db.datasets.find_one({"_id": ObjectId(self.dataset_id)})

        # Verify the fields were updated correctly
        self.assertEqual(updated_dataset['name'], "Updated Dataset Name")
        self.assertEqual(updated_dataset['description'], "This is an updated description.")

    def test_update_dataset_not_found(self):
        # Test updating a non-existent dataset
        non_existent_dataset_id = str(ObjectId())
        update_data = {
            "name": "Updated Dataset Name",
            "description": "This is an updated description."
        }
        response = self.client.put(f'/datasets/{non_existent_dataset_id}', json=update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dataset not found", response.data.decode())

    def test_delete_dataset(self):
        # Delete the dataset using its ID from setup
        response = self.client.delete(f'/datasets/{self.dataset_id}')
        self.assertEqual(response.status_code, 200)

        # Verify the dataset was deleted
        deleted_dataset = self.app.db.datasets.find_one({"_id": ObjectId(self.dataset_id)})
        self.assertIsNone(deleted_dataset)

    def test_delete_dataset_not_found(self):
        # Test deleting a non-existent dataset
        non_existent_dataset_id = str(ObjectId())
        response = self.client.delete(f'/datasets/{non_existent_dataset_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dataset not found", response.data.decode())

if __name__ == '__main__':
    unittest.main()
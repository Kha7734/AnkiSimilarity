import unittest
from flask import json
from bson import ObjectId
from app import create_app

class TestUserSettingRoutes(unittest.TestCase):

    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test client
        self.client = self.app.test_client()

        # Clear the settings collection in the test database
        self.app.db.settings.delete_many({})

        # Set up test data
        self.user_id = str(ObjectId())
        self.test_settings_data = {
            "user_id": self.user_id,
            "language_preference": "en",
            "daily_goal": 20,
            "notification_enabled": True,
            "notification_time": "09:00",
            "theme": "light"
        }

        # Insert the test settings into the database
        response = self.client.post('/settings', json=self.test_settings_data)
        self.assertEqual(response.status_code, 201, msg=f"Failed to create test settings. Response: {response.data.decode()}")

        # Get the settings ID from the response data
        self.settings_id = json.loads(response.data)['settings_id']

    def tearDown(self):
        # Clean up after each test by deleting any settings created during tests
        self.app.db.settings.delete_many({})

        # Pop the app context
        self.app_context.pop()

    def test_create_settings(self):
        # Test creating a new settings record
        new_settings_data = {
            "user_id": str(ObjectId()),
            "language_preference": "vi",
            "daily_goal": 30,
            "notification_enabled": False,
            "notification_time": "10:00",
            "theme": "dark"
        }
        response = self.client.post('/settings', json=new_settings_data)
        self.assertEqual(response.status_code, 201)

        # Verify the settings were created
        settings_id = json.loads(response.data)['settings_id']
        settings = self.app.db.settings.find_one({"_id": ObjectId(settings_id)})
        self.assertIsNotNone(settings)
        self.assertEqual(settings['language_preference'], "vi")
        self.assertEqual(settings['daily_goal'], 30)

    def test_get_settings(self):
        # Retrieve the settings using the user ID from setup
        response = self.client.get(f'/settings/{self.user_id}')
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Verify the returned data matches the test data
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], self.user_id)
        self.assertEqual(data['language_preference'], "en")
        self.assertEqual(data['daily_goal'], 20)
        self.assertEqual(data['notification_enabled'], True)
        self.assertEqual(data['notification_time'], "09:00")
        self.assertEqual(data['theme'], "light")

    def test_get_settings_not_found(self):
        # Test retrieving settings for a non-existent user
        non_existent_user_id = str(ObjectId())
        response = self.client.get(f'/settings/{non_existent_user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Settings not found", response.data.decode())

    def test_update_settings(self):
        # Update the settings using the user ID from setup
        update_data = {
            "language_preference": "vi",
            "daily_goal": 30,
            "notification_enabled": False,
            "notification_time": "10:00",
            "theme": "dark"
        }
        response = self.client.put(f'/settings/{self.user_id}', json=update_data)

        # Ensure the update request was successful
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}")

        # Retrieve the updated settings
        updated_settings = self.app.db.settings.find_one({"user_id": self.user_id})

        # Verify the fields were updated correctly
        self.assertEqual(updated_settings['language_preference'], "vi")
        self.assertEqual(updated_settings['daily_goal'], 30)
        self.assertEqual(updated_settings['notification_enabled'], False)
        self.assertEqual(updated_settings['notification_time'], "10:00")
        self.assertEqual(updated_settings['theme'], "dark")

    def test_update_settings_not_found(self):
        # Test updating settings for a non-existent user
        non_existent_user_id = str(ObjectId())
        update_data = {
            "language_preference": "vi",
            "daily_goal": 30
        }
        response = self.client.put(f'/settings/{non_existent_user_id}', json=update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Settings not found", response.data.decode())

    def test_delete_settings(self):
        # Delete the settings using the user ID from setup
        response = self.client.delete(f'/settings/{self.user_id}')
        self.assertEqual(response.status_code, 200)

        # Verify the settings were deleted
        deleted_settings = self.app.db.settings.find_one({"user_id": self.user_id})
        self.assertIsNone(deleted_settings)

    def test_delete_settings_not_found(self):
        # Test deleting settings for a non-existent user
        non_existent_user_id = str(ObjectId())
        response = self.client.delete(f'/settings/{non_existent_user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Settings not found", response.data.decode())

if __name__ == '__main__':
    unittest.main()
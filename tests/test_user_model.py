import unittest
from bson import ObjectId
from app import create_app  # Import your create_app function
from app.models.user import User
from app.databases.db import close_db  # Import close_db for cleanup

class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Create the Flask app with the testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the application context

        # Clear the users collection in the test database
        self.app.db.users.delete_many({})

        # Set up a test user in the database before each test
        self.test_username = "testuser"
        self.test_email = "test@example.com"
        self.test_password = "password123"
        self.user = User.create_user(self.test_username, self.test_email, self.test_password)

    def tearDown(self):
        # Clean up after each test by deleting the test user
        self.app.db.users.delete_many({})  # Clear the users collection

        # Close the database connection
        close_db()

        # Pop the application context
        self.app_context.pop()

    def test_create_user(self):
        # Retrieve the user from the database
        user = self.app.db.users.find_one({"username": self.test_username})
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], self.test_email)

    def test_validate_user(self):
        # Validate the user's credentials
        is_valid = User.validate_user(self.test_username, self.test_password)
        self.assertTrue(is_valid)

    def test_invalid_login(self):
        # Test invalid login credentials
        is_valid = User.validate_user(self.test_username, "wrongpassword")
        self.assertFalse(is_valid)

    def test_check_username_exists(self):
        # Check if the username exists
        exists = User.check_username_exists(self.test_username)
        self.assertTrue(exists)

    def test_check_email_exists(self):
        # Check if the email exists
        exists = User.check_email_exists(self.test_email)
        self.assertTrue(exists)

if __name__ == '__main__':
    unittest.main()
# tests/test_user_model.py

import unittest
from app.models.user import User
from flask import current_app
from app import create_app

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the application context

        # Set up a test user in the database before each test
        self.test_username = "testuser"
        self.test_email = "test@example.com"
        self.test_password = "password123"
        self.user = User.create_user(self.test_username, self.test_email, self.test_password)

    def tearDown(self):
        # Clean up after each test by deleting the test user
        User.delete_user(self.user.user_id)  # Use the user ID of the created user
        self.app_context.pop()  # Pop the application context

    def test_create_user(self):
        user = current_app.db.users.find_one({"username": self.test_username})
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], self.test_email)

    def test_validate_user(self):
        is_valid = User.validate_user(self.test_username, self.test_password)
        self.assertTrue(is_valid)

    def test_invalid_login(self):
        is_valid = User.validate_user(self.test_username, "wrongpassword")
        self.assertFalse(is_valid)

    def test_check_username_exists(self):
        exists = User.check_username_exists(self.test_username)
        self.assertTrue(exists)

    def test_check_email_exists(self):
        exists = User.check_email_exists(self.test_email)
        self.assertTrue(exists)

if __name__ == '__main__':
    unittest.main()

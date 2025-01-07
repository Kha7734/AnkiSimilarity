import unittest
from bson import ObjectId
from app.models.user_setting import UserSettings
from app import create_app, close_db

class TestUserSettingModel(unittest.TestCase):
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

        # Close the database connection
        close_db()

        self.app_context.pop()

    def test_create_user_setting(self):
        settings = UserSettings(
            user_id=self.user_id,
            language_preference="en",
            daily_goal=20,
            notification_enabled=True,
            notification_time="09:00",
            theme="light"
        )
        settings_dict = settings.to_dict()
        self.assertIn('_id', settings_dict)
        self.assertEqual(settings_dict['user_id'], self.user_id)
        self.assertEqual(settings_dict['language_preference'], "en")
        self.assertEqual(settings_dict['daily_goal'], 20)
        self.assertEqual(settings_dict['notification_enabled'], True)
        self.assertEqual(settings_dict['notification_time'], "09:00")
        self.assertEqual(settings_dict['theme'], "light")

    def test_save_user_setting(self):
        settings = UserSettings(
            user_id=self.user_id,
            language_preference="en",
            daily_goal=20,
            notification_enabled=True,
            notification_time="09:00",
            theme="light"
        )
        settings_id = self.test_db.settings.insert_one(settings.to_dict()).inserted_id
        saved_settings = self.test_db.settings.find_one({"_id": settings_id})
        self.assertIsNotNone(saved_settings)
        self.assertEqual(saved_settings['language_preference'], "en")

if __name__ == '__main__':
    unittest.main()
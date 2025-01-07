from bson import ObjectId

class UserSettings:
    def __init__(self, user_id, language_preference="en", daily_goal=20, notification_enabled=True, notification_time="09:00", theme="light"):
        self.settings_id = ObjectId()
        self.user_id = user_id
        self.language_preference = language_preference
        self.daily_goal = daily_goal
        self.notification_enabled = notification_enabled
        self.notification_time = notification_time
        self.theme = theme

    def to_dict(self):
        return {
            "_id": self.settings_id,
            "user_id": self.user_id,
            "language_preference": self.language_preference,
            "daily_goal": self.daily_goal,
            "notification_enabled": self.notification_enabled,
            "notification_time": self.notification_time,
            "theme": self.theme
        }
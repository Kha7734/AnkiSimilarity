from datetime import datetime
from bson import ObjectId

class UserProgress:
    def __init__(self, user_id, card_id, dataset_id, status="new"):
        self.progress_id = ObjectId()
        self.user_id = user_id
        self.card_id = card_id
        self.dataset_id = dataset_id
        self.status = status
        self.last_reviewed = None
        self.next_review = None
        self.streak = 0
        self.ease_factor = 2.5  # Default ease factor for spaced repetition
        self.interval = 1  # Default interval in days

    def to_dict(self):
        return {
            "_id": self.progress_id,
            "user_id": self.user_id,
            "card_id": self.card_id,
            "dataset_id": self.dataset_id,
            "status": self.status,
            "last_reviewed": self.last_reviewed,
            "next_review": self.next_review,
            "streak": self.streak,
            "ease_factor": self.ease_factor,
            "interval": self.interval
        }
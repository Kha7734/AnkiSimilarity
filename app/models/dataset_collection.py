from datetime import datetime
from bson import ObjectId

class Dataset:
    def __init__(self, user_id, name, description):
        self.dataset_id = ObjectId()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self.dataset_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_NAME]
        self.users = self.db.users

    def create_user(self, email, username, hashed_password):
        user = {
            'email': email,
            'username': username,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            'is_active': True
        }
        result = self.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user

    def get_user_by_email(self, email):
        return self.users.find_one({'email': email})

    def email_exists(self, email):
        return self.users.count_documents({'email': email}) > 0
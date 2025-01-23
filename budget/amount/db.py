from pymongo import MongoClient
from django.conf import settings
from datetime import datetime
from bson import ObjectId

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_NAME]
        self.users = self.db.users
        self.incomes = self.db.incomes
        

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
    
    def create_income(self, user_id, amount, description, date):
        income = {
            'user_id': user_id,
            'amount': amount,
            'description': description,
            'date': date,
            'created_at': datetime.utcnow()
        }
        result = self.incomes.insert_one(income)
        income['_id'] = str(result.insert_id)
        return income
    def get_incomes_by_user(self, user_id):
        return list(self.incomes.find({'user_id': user_id}))

    def get_income_by_id(self, income_id):
        return self.incomes.find_one({'_id': ObjectId(income_id)})

    def update_income(self, income_id, amount, description, date):
        result = self.incomes.update_one(
            {'_id': ObjectId(income_id)},
            {'$set': {
                'amount': amount,
                'description': description,
                'date': date,
                'updated_at': datetime.utcnow()
            }}
        )
        return result.modified_count > 0

    def delete_income(self, income_id):
        result = self.incomes.delete_one({'_id': ObjectId(income_id)})
        return result.deleted_count > 0
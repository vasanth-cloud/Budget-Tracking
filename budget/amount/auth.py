import jwt
from datetime import datetime, timedelta
from django.conf import settings

class JWTAuth:
    @staticmethod
    def create_token(user_id):
        access_token_payload = {
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        
        refresh_token_payload = {
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }

        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

        return {
            'access': access_token,
            'refresh': refresh_token
        }
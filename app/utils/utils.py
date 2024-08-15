# app/utils.py
from datetime import datetime, timedelta
import jwt
from flask import current_app as app

def generate_recovery_link(user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
    return f"http://example.com/recovery?token={token}"

def send_email(to_email, recovery_link):
    # Implementar o envio de e-mail aqui
    pass

def validate_token(token, user_id):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id'] == user_id
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

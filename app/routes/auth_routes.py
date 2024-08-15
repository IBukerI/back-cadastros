from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from app.repositories.auth_repository import find_password_by_user
from app.repositories.user_repository import find_user_by_email_return_id
import bcrypt
import jwt
from datetime import datetime, timedelta

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    stored_hash = find_password_by_user(email)
    
    if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        
        user_code = find_user_by_email_return_id(email)
        token = jwt.encode(
            {
                'email': email,
                'user_code': user_code,
                'exp': datetime.utcnow() + timedelta(minutes=800)  
            }, 
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.auth import token_required
from app.repositories.user_repository import find_user_by_email, find_user_by_cpf, find_user_by_id, return_user_list
import bcrypt

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/create', methods=['POST'])
@token_required
def create_user(user_code):
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha_hash = data.get('senha')
    cpf = data.get('cpf')
    create_user = user_code
    
    if not nome or not email or not senha_hash or not cpf:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if find_user_by_email(email):
        return jsonify({'message': 'Este e-mail já está cadastrado'}), 400
    if find_user_by_cpf(cpf):
        return jsonify({'message': 'Este CPF já está cadastrado'}), 400

    hashed_password = bcrypt.hashpw(senha_hash.encode('utf-8'), bcrypt.gensalt())
    
    try:
        new_user = User(
            nome=nome, 
            email=email, 
            senha_hash=hashed_password.decode('utf-8'), 
            cpf=cpf, 
            created_by=create_user, 
            ativo=1,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}), 500

@user_routes.route('/users', methods=['GET'])
@token_required
def get_user(user_code):
    
    users = return_user_list()
    
    return jsonify({'users': users}), 200

@user_routes.route('/inativar-usuario', methods=['POST'])
@token_required
def inativar_user(user_code):
    data = request.get_json()
    id = data.get('id')

    if id is None:
        return jsonify({'message': 'ID do usuário não fornecido'}), 400

    user_para_inativar = find_user_by_id(id)

    if user_para_inativar is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if user_para_inativar.ativo == 1:
        try:
            user_para_inativar.ativo = 0
            user_para_inativar.updated_at = datetime.now()
            user_para_inativar.updated_by = user_code
            
            db.session.commit()
            return jsonify({'message': 'Usuário inativado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {e}'}), 500
    else:
        return jsonify({'message': 'Usuário já está inativo'}), 400

@user_routes.route('/ativar-usuario', methods=['POST'])
@token_required
def ativar_user(user_code):
    data = request.get_json()
    id = data.get('id')

    if id is None:
        return jsonify({'message': 'ID do usuário não fornecido'}), 400

    user_para_ativar = find_user_by_id(id)

    if user_para_ativar is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if user_para_ativar.ativo == 0:
        try:
            user_para_ativar.ativo = 1
            user_para_ativar.updated_at = datetime.now()
            user_para_ativar.updated_by = user_code
            
            db.session.commit()
            return jsonify({'message': 'Usuário ativado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {e}'}), 500
    else:
        return jsonify({'message': 'Usuário já está ativo'}), 400

    
@user_routes.route('/atualizar-usuario', methods=['PUT'])
@token_required
def atualizar_user(user_code):
    data = request.get_json()
    id = data.get('id')
    
    if id is None:
        return jsonify({'message': 'ID do usuário não fornecido'}), 400

    user_para_atualizar = find_user_by_id(id)

    if user_para_atualizar is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    
    updated_fields = ['nome', 'email', 'senha']
    try:
        for field in updated_fields:
            if field in data:
                if field == 'senha':
                    hashed_password = bcrypt.hashpw(data[field].encode('utf-8'), bcrypt.gensalt())
                    setattr(user_para_atualizar, 'senha_hash', hashed_password.decode('utf-8'))
                else:
                    setattr(user_para_atualizar, field, data[field])
        
        user_para_atualizar.updated_at = datetime.now()
        user_para_atualizar.updated_by = user_code
        
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}), 500
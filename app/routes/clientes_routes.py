from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente, Endereco, Telefone, Email
from app.auth import token_required
from app.repositories.clientes_repository import obter_clientes_ativos, obter_clientes_por_cpf, obter_clientes_por_cnpj


clientes_routes = Blueprint('clientes_routes', __name__)


@clientes_routes.route('/clientes', methods=['GET'])
@token_required
def todos_clientes(user_code):
    
    clientes = obter_clientes_ativos()
    
    return jsonify({'clientes': clientes}), 200


@clientes_routes.route('/criar', methods=['POST'])
@token_required
def criar_clientes(user_code):
    data = request.get_json()
    
    tipo = data['tipo']
    novo_cliente = None
    
    if tipo == '1':
        existe_cliente = obter_clientes_por_cpf(data['cpf'], None)
        if existe_cliente:
            return jsonify({'message': 'Usuário já cadastrado com esse CPF'}), 2000
        
        novo_cliente = Cliente(
            nome=data['nome'],
            cpf= data['cpf'],
            tipo_cliente= 1,            
            data_criacao=datetime.now(),
            created_by=user_code,
            ativo=1,
        )
    
    elif tipo == '2':
        existe_cliente = obter_clientes_por_cnpj(data['cnpj'], None)
        if existe_cliente:
            return jsonify({'message': 'CNPJ já cadastrado'}), 200
        novo_cliente = Cliente(
            nome=data['nome'],             
            razao_social = data['razao_social'], 
            cnpj = data['cnpj'], 
            inscr_estadual = data['inscr_estadual'], 
            inscr_municipal = data['inscr_municipal'], 
            tipo_cliente=2,            
            data_criacao=datetime.now(),
            created_by=user_code,
            ativo=1,
        )
    
    if novo_cliente:
        db.session.add(novo_cliente)
        db.session.commit()
        
        

        if 'telefones' in data:
            for telefone in data['telefones']:
                numero_telefone = telefone['telefone']                    
                novo_telefone = Telefone(
                    cliente=novo_cliente.id,                   
                    telefone=numero_telefone,
                    data_criacao=datetime.now(),
                    created_by=user_code,
                    ativo=1
                )
                db.session.add(novo_telefone)
        
        if 'emails' in data:
            for email in data['emails']:
                email_str = email['email']                    
                novo_email = Email(
                    cliente=novo_cliente.id,
                    email=email_str,
                    data_criacao=datetime.now(),
                    created_by=user_code,
                    ativo=1
                )
                db.session.add(novo_email)
        
        if 'endereco' in data:
            endereco = data['endereco']
            novo_endereco = Endereco(
                cliente=novo_cliente.id,
                rua=endereco['rua'],
                numero=endereco['numero'],
                complemento=endereco['complemento'],
                cep=endereco['cep'],
                bairro=endereco['bairro'],
                cidade=endereco['cidade'],                
                estado=endereco['estado'],
                data_criacao=datetime.now(),
                created_by=user_code,
                ativo=1
            )
            db.session.add(novo_endereco)
        
        db.session.commit()  

        return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 201
    
    return jsonify({'message': 'Tipo de cliente inválido'}), 400

@clientes_routes.route('/obter-cliente-por-cpf', methods=['GET'])
@token_required
def obter_cliente_por_cpf(user_code):
    data = request.get_json()
    
    cpf = data['cpf']
    cliente = obter_clientes_por_cpf(cpf, None)
    
    if cliente:
        return jsonify({'cliente': cliente}), 200
    
    return jsonify({'message': 'Cliente não encontrado'}), 404

@clientes_routes.route('/obter-cliente-por-cnpj', methods=['GET'])
@token_required
def obter_cliente_por_cnpj(user_code):
    data = request.get_json()
    
    cnpj = data['cnpj']
    cliente = obter_clientes_por_cnpj(cnpj, None)
    
    if cliente:
        return jsonify({'cliente': cliente}), 200
    
    return jsonify({'message': 'Cliente não encontrado'}), 404
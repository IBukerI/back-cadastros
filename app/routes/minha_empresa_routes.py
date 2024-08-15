from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import MinhaEmpresa, MeusEmails, MeusTelefones
from app.auth import token_required
from app.repositories.minha_empresa_repository import obter_empresas_ativas, obter_empresa_por_cnpj,  obter_telefone_por_empresa_id_e_numero, obter_email_por_empresa_id_e_email, obter_empresa_por_id
from app.repositories.minha_empresa_repository import obter_telefone_por_id, obter_email_por_id, obter_empresa_por_id_desativadas


minha_empresa_routes = Blueprint('minha_empresa', __name__)

@minha_empresa_routes.route('/empresas', methods=['GET'])
@token_required
def get_empresas(user_code):
    
    empresas = obter_empresas_ativas()
    
    return jsonify({'Empresas': empresas}), 200

@minha_empresa_routes.route('/criar', methods=['POST'])
@token_required
def criar_empresa(user_code):
    data = request.get_json()    

    nova_empresa = MinhaEmpresa(
        nome=data['nome'],
        razao_social=data['razao_social'],
        cnpj=data['cnpj'],
        inscr_estadual=data['inscr_estadual'],
        inscr_municipal=data['inscr_municipal'],
        rua=data['rua'],
        numero=data['numero'],
        complemento=data['complemento'],
        cep=data['cep'],
        bairro=data['bairro'],
        cidade=data['cidade'],
        estado=data['estado'],        
        data_criacao=datetime.now(),
        created_by=user_code,
        ativo=1
    )
    
    empresa_existe = obter_empresa_por_cnpj(data['cnpj'])
    if not empresa_existe:
        db.session.add(nova_empresa)
        db.session.commit()
    
        empresa_id = nova_empresa.id
    
        if 'telefones' in data:
            for telefone in data['telefones']:
                numero_telefone = telefone['telefone']
                telefone_existe = obter_telefone_por_empresa_id_e_numero(empresa_id, numero_telefone)
                if not telefone_existe:
                    novo_telefone = MeusTelefones(
                        id_minha_empresa=empresa_id,
                        telefone=numero_telefone,
                        data_criacao=datetime.now(),
                        created_by=user_code,
                        ativo=1
                    )
                    db.session.add(novo_telefone)
                
        if 'emails' in data:
            for email in data['emails']:
                email_str = email['email']
                email_existe = obter_email_por_empresa_id_e_email(empresa_id, email_str)
                if not email_existe:
                    novo_email = MeusEmails(
                        id_minha_empresa=empresa_id,
                        email=email_str,
                        data_criacao=datetime.now(),
                        created_by=user_code,
                        ativo=1
                    )
                    db.session.add(novo_email)
                
        db.session.commit()  

        return jsonify({'message': 'Empresa cadastrada com sucesso!'}), 201
    else:
        return jsonify({'message': 'Empresa já cadastrada!'}), 400

@minha_empresa_routes.route('/desativar', methods=['PUT'])
@token_required
def desativar_empresa(user_code):
    data = request.get_json()    
    empresa_id = data.get('id')
    
    empresa = obter_empresa_por_id(empresa_id)
    if empresa and empresa.ativo == 1: 
        empresa.ativo = 0
        empresa.updated_at = datetime.now()
        empresa.updated_by = user_code
        db.session.commit()
        return jsonify({'message': 'Empresa desativada com sucesso!'}), 200
    else:
        return jsonify({'message': 'Empresa não encontrada ou já desativada!'}), 404

@minha_empresa_routes.route('/atualizar', methods=['PUT'])
@token_required
def atualizar_empresa(user_code):
    data = request.get_json()
    empresa_id = data.get('id')
        
    if empresa_id is None:
        return jsonify({'message': 'ID da Empresa não fornecida'}), 400
    
    empresa_para_atualizar = obter_empresa_por_id(empresa_id)
    
    if empresa_para_atualizar is None:
        return jsonify({'message': 'Empresa não encontrada'}), 404
   
    updated_fields = ['nome', 'razao_social', 'inscr_estadual', 'inscr_municipal', 'rua', 'numero', 'complemento', 'cep', 'bairro', 'cidade', 'estado']
    
    try:
        
        for field in updated_fields:
            if field in data:
                setattr(empresa_para_atualizar, field, data[field])              
        
        empresa_para_atualizar.updated_at = datetime.now()
        empresa_para_atualizar.updated_by = user_code
        
        
        if 'telefones' in data:
            telefones_atualizar = {tel['telefone'] for tel in data['telefones']}
            telefones_existentes = obter_telefone_por_id(empresa_id)
            
            
            for telefone in data['telefones']:
                telefone_atual = next((t for t in telefones_existentes if t.telefone == telefone['telefone']), None)
                if telefone_atual:
                    telefone_atual.telefone = telefone['telefone']
                    telefone_atual.updated_at = datetime.now()
                    telefone_atual.updated_by = user_code
                else:
                    novo_telefone = MeusTelefones(
                        id_minha_empresa=empresa_id,
                        telefone=telefone['telefone'],
                        data_criacao=datetime.now(),
                        created_by=user_code,
                        ativo=1
                    )
                    db.session.add(novo_telefone)

            
            telefones_existentes_para_remover = [t for t in telefones_existentes if t.telefone not in telefones_atualizar]
            for telefone in telefones_existentes_para_remover:
                db.session.delete(telefone)

        
        if 'emails' in data:
            emails_atualizar = {email['email'] for email in data['emails']}
            emails_existentes = obter_email_por_id(empresa_id)
            
            
            for email in data['emails']:
                email_atual = next((e for e in emails_existentes if e.email == email['email']), None)
                if email_atual:
                    email_atual.email = email['email']
                    email_atual.updated_at = datetime.now()
                    email_atual.updated_by = user_code
                else:
                    novo_email = MeusEmails(
                        id_minha_empresa=empresa_id,
                        email=email['email'],
                        data_criacao=datetime.now(),
                        created_by=user_code,
                        ativo=1
                    )
                    db.session.add(novo_email)

           
            emails_existentes_para_remover = [e for e in emails_existentes if e.email not in emails_atualizar]
            for email in emails_existentes_para_remover:
                db.session.delete(email)

        db.session.commit()
        return jsonify({'message': 'Empresa e informações relacionadas atualizadas com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}), 500

@minha_empresa_routes.route('/ativar', methods=['PUT'])
@token_required
def ativar_empresa(user_code):
    data = request.get_json()    
    empresa_id = data.get('id')
    
    empresa = obter_empresa_por_id_desativadas(empresa_id)
    if empresa and empresa.ativo == 0: 
        empresa.ativo = 1
        empresa.updated_at = datetime.now()
        empresa.updated_by = user_code
        db.session.commit()
        return jsonify({'message': 'Empresa ativada com sucesso!'}), 200
    else:
        return jsonify({'message': 'Empresa não encontrada ou já ativa!'}), 404
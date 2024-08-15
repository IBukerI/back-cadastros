from app import db
from app.models import MinhaEmpresa, MeusEmails, MeusTelefones
from sqlalchemy import select

def obter_empresas_ativas():
    stmt = (
        select(
            MinhaEmpresa.id,
            MinhaEmpresa.nome,
            MinhaEmpresa.razao_social,
            MinhaEmpresa.cnpj,
            MinhaEmpresa.inscr_estadual,
            MinhaEmpresa.inscr_municipal,
            MinhaEmpresa.bairro,
            MinhaEmpresa.cep,
            MinhaEmpresa.cidade,
            MinhaEmpresa.estado,
            MinhaEmpresa.rua,
            MinhaEmpresa.numero,
            MinhaEmpresa.complemento,
            MinhaEmpresa.data_criacao,
            MinhaEmpresa.created_by
        )
        .filter(MinhaEmpresa.ativo == 1)
    )
    
    empresas_ativas = db.session.execute(stmt).fetchall()  
    resultado = []

    for empresa in empresas_ativas:
        telefones_ativos = db.session.execute(
            select(
                MeusTelefones.id,
                MeusTelefones.telefone,
                MeusTelefones.data_criacao,
                MeusTelefones.created_by
            )
            .filter(MeusTelefones.id_minha_empresa == empresa.id, MeusTelefones.ativo == 1)
        ).fetchall()

        emails_ativos = db.session.execute(
            select(
                MeusEmails.id,
                MeusEmails.email,
                MeusEmails.data_criacao,
                MeusEmails.created_by
            )
            .filter(MeusEmails.id_minha_empresa == empresa.id, MeusEmails.ativo == 1)
        ).fetchall()

        resultado.append({
            'empresa': {
                'id': empresa.id,
                'nome': empresa.nome,
                'razao_social': empresa.razao_social,
                'cnpj': empresa.cnpj,
                'inscr_estadual': empresa.inscr_estadual,
                'inscr_municipal': empresa.inscr_municipal,
                'bairro': empresa.bairro,
                'cep': empresa.cep,
                'cidade': empresa.cidade,
                'estado': empresa.estado,
                'rua': empresa.rua,
                'numero': empresa.numero,
                'complemento': empresa.complemento,
                'data_criacao': empresa.data_criacao,
                'created_by': empresa.created_by,
            },
            'telefones': [
                {
                    'id': telefone.id,
                    'telefone': telefone.telefone,
                    'data_criacao': telefone.data_criacao,
                    'created_by': telefone.created_by,
                }
                for telefone in telefones_ativos
            ],
            'emails': [
                {
                    'id': email.id,
                    'email': email.email,
                    'data_criacao': email.data_criacao,
                    'created_by': email.created_by,
                }
                for email in emails_ativos
            ]
        })

    return resultado

def obter_empresa_por_cnpj(cnpj):
    empresa = MinhaEmpresa.query.filter_by(cnpj=cnpj).first()
    return empresa

def obter_telefone_por_empresa_id_e_numero(id_minha_empresa, numero):
    telefone = MeusTelefones.query.filter_by(id_minha_empresa=id_minha_empresa, telefone=numero, ativo=1).first()
    return telefone

def obter_email_por_id(id):
    email = MeusEmails.query.filter_by(id_minha_empresa=id, ativo=1).all()
    return email

def obter_telefone_por_id(id):
    telefone = MeusTelefones.query.filter_by(id_minha_empresa=id, ativo=1).all()
    return telefone

def obter_email_por_empresa_id_e_email(id_minha_empresa, email):
    email_registrado = MeusEmails.query.filter_by(id_minha_empresa=id_minha_empresa, email=email, ativo=1).first()
    return email_registrado

def obter_empresa_por_id(id):
    empresa = MinhaEmpresa.query.filter_by(id=id, ativo=1).first()
    return empresa

def obter_empresa_por_id_desativadas(id):
    empresa = MinhaEmpresa.query.filter_by(id=id, ativo=0).first()
    return empresa
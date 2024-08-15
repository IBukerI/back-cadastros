from app import db
from app.models import Cliente, Endereco, Telefone, Email
from sqlalchemy import select


def obter_clientes_ativos():
    stmt = (
        select(
            Cliente.id,
            Cliente.nome,
            Cliente.ativo,
            Cliente.data_criacao,
            Cliente.created_by,
            Cliente.tipo_cliente,
            Cliente.cnpj,
            Cliente.razao_social,
            Cliente.cpf,
            Cliente.inscr_estadual,
            Cliente.inscr_municipal
        )
        .filter(Cliente.ativo == 1)
    )
    
    clientes_ativos = db.session.execute(stmt).fetchall()  
    resultado = []
    
    for cliente in clientes_ativos:       
        endereco_ativo = db.session.execute(
            select(
                Endereco.id,
                Endereco.rua,
                Endereco.numero,
                Endereco.complemento,
                Endereco.cep,
                Endereco.bairro,
                Endereco.cidade,
                Endereco.estado
            )
            .filter(Endereco.cliente == cliente.id, Endereco.ativo == 1)
        ).fetchall()
        
        telefones_ativos = db.session.execute(
            select(
                Telefone.id,
                Telefone.telefone,
                Telefone.data_criacao               
            )
            .filter(Telefone.cliente == cliente.id, Telefone.ativo == 1)
        ).fetchall()
        
        emails_ativos = db.session.execute( 
            select(
                Email.id,
                Email.email,
                Email.data_criacao                
            )
            .filter(Email.cliente == cliente.id, Email.ativo == 1)
        ).fetchall()
        
        resultado.append({
            'cliente': {
                'id': cliente.id,
                'nome': cliente.nome,
                'ativo': cliente.ativo,                
                'data_criacao': cliente.data_criacao,
                'created_by': cliente.created_by,
                'cpf': cliente.cpf,
                'cnpj': cliente.cnpj,
                'razao_social': cliente.razao_social,
                'inscr_estadual': cliente.inscr_estadual,
                'inscr_municipal': cliente.inscr_municipal
            },
            'telefones': [
                {
                    'id': telefone.id,
                    'telefone': telefone.telefone,
                    'data_criacao': telefone.data_criacao
                }
                for telefone in telefones_ativos
            ],
            'emails': [
                {
                    'id': email.id,
                    'email': email.email,
                    'data_criacao': email.data_criacao
                }
                for email in emails_ativos
            ],
            'enderecos': [
                {
                    'id': endereco.id,
                    'rua': endereco.rua,
                    'numero': endereco.numero,
                    'complemento': endereco.complemento,
                    'cep': endereco.cep,
                    'bairro': endereco.bairro,
                    'cidade': endereco.cidade,
                    'estado': endereco.estado
                }
                for endereco in endereco_ativo
            ]
        })
    
    return resultado

def obter_clientes_ativos_por_id(cliente_id):
    stmt = (
        select(
            Cliente.id,
            Cliente.nome,            
            Cliente.tipo,
            Cliente.cnpj,
            Cliente.razao_social,
            Cliente.cpf,
            Cliente.ativo,
            Cliente.data_criacao,
            Cliente.created_by
        )
        .filter(Cliente.id == cliente_id, Cliente.ativo == 1)
    )
    
    cliente = db.session.execute(stmt).fetchone()   

    endereco_ativo = db.session.execute(
        select(
            Endereco.id,
            Endereco.rua,
            Endereco.numero,
            Endereco.complemento,
            Endereco.cep,
            Endereco.bairro,
            Endereco.cidade,
            Endereco.estado
        )
        .filter(Endereco.cliente == cliente.id, Endereco.ativo == 1)
    ).fetchall()
    
    telefones_ativos = db.session.execute(
        select(
            Telefone.id,
            Telefone.telefone,                         
        )
        .filter(Telefone.cliente == cliente.id, Telefone.ativo == 1)
    ).fetchall()
    
    emails_ativos = db.session.execute( 
        select(
            Email.id,
            Email.email                           
        )
        .filter(Email.cliente == cliente.id, Email.ativo == 1)
    ).fetchall()
    
    resultado = {
        'cliente': {
            'id': cliente.id,
            'nome': cliente.nome,
            'ativo': cliente.ativo,
            'cliente_tipo': cliente.tipo,
            'cnpj': cliente.cnpj,
            'razao_social': cliente.razao_social,
            'cpf': cliente.cpf,              
            'data_criacao': cliente.data_criacao,
            'created_by': cliente.created_by,            
            'enderecos': [dict(endereco) for endereco in endereco_ativo],
            'telefones': [dict(telefone) for telefone in telefones_ativos],
            'emails': [dict(email) for email in emails_ativos]
        }
    }

    return resultado

def obter_clientes_por_cpf(cpf, status):
    stmt = (
        select(
            Cliente.id,
            Cliente.cpf,            
            Cliente.nome, 
            Cliente.created_by,          
        )
        .filter(Cliente.cpf == cpf)
    )
    
    if status is not None:
        stmt = stmt.filter(Cliente.ativo == status)
    
    clientes = db.session.execute(stmt).fetchall()
    
    resultado = []
    for cliente in clientes:
        enderecos_ativos = obter_enderecos_ativos(Cliente.id)
        emails_ativos = obter_emails_ativos(Cliente.id)
        telefones_ativos = obter_telefones_ativos(Cliente.id)
        
        resultado.append({
            'cliente': {
                'id': cliente.id,
                'nome': cliente.nome,                
                'cpf': cliente.cpf,
                'created_by': cliente.created_by,                               
                'enderecos': [dict(endereco._mapping) for endereco in enderecos_ativos],
                'telefones': [dict(telefone._mapping) for telefone in telefones_ativos],
                'emails': [dict(email._mapping) for email in emails_ativos]
            }
        })
    
    return resultado

def obter_clientes_por_cnpj(cnpj, status):
    stmt = select(
        Cliente.id,
        Cliente.cnpj,
        Cliente.razao_social,    
    ).filter(Cliente.cnpj == cnpj)
    
    if status is not None:
        stmt = stmt.filter(Cliente.ativo == status)
    
    clientes = db.session.execute(stmt).fetchall()
    
    if status is not None:
        stmt = stmt.filter(Cliente.ativo == status)
    
    clientes = db.session.execute(stmt).fetchall()
    
    resultado = []
    for cliente_ativo in clientes:
        enderecos_ativos = obter_enderecos_ativos(Cliente.id)
        emails_ativos = obter_emails_ativos(Cliente.id)
        telefones_ativos = obter_telefones_ativos(Cliente.id)
        
        resultado.append({
            'cliente': {
                'id': cliente_ativo.id,
                'nome': cliente_ativo.nome,
                'razao_social': cliente_ativo.razao_social,
                'ativo': cliente_ativo.ativo,
                'data_criacao': cliente_ativo.data_criacao,
                'created_by': cliente_ativo.created_by,
                'cnpj': cliente_ativo.cnpj,                
                'enderecos': [dict(endereco._mapping) for endereco in enderecos_ativos],
                'telefones': [dict(telefone._mapping) for telefone in telefones_ativos],
                'emails': [dict(email._mapping) for email in emails_ativos]
            }
        })
    
    return resultado

def obter_enderecos_ativos(id_cliente):
    return db.session.execute(
        select(
            Endereco.id,
            Endereco.rua,
            Endereco.numero,
            Endereco.complemento,
            Endereco.cep,
            Endereco.bairro,
            Endereco.cidade,
            Endereco.estado
        ).filter(Endereco.cliente == id_cliente, Endereco.ativo == 1)
    ).fetchall()

def obter_emails_ativos(id_cliente):
    return db.session.execute(
        select(
            Email.id,
            Email.email,
            Email.data_criacao
        ).filter(Email.cliente== id_cliente, Email.ativo == 1)
    ).fetchall()

def obter_telefones_ativos(id_cliente):
    return db.session.execute(
        select(
            Telefone.id,
            Telefone.telefone,
            Telefone.data_criacao
        ).filter(Telefone.cliente == id_cliente, Telefone.ativo == 1)
    ).fetchall()
              
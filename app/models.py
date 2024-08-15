from app import db
from sqlalchemy import Column, Integer, String, DateTime,func
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(128), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    ativo = Column(Integer, default=True)
    updated_by = Column(Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'ativo': self.ativo,
            'updated_by': self.updated_by
        }

class Roles(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)   

    def __repr__(self):
        return f'<Role {self.name}>'
    
class MinhaEmpresa(db.Model):
    __tablename__ = 'minha_empresa'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    razao_social = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    inscr_estadual = Column(String(20), nullable=False)
    inscr_municipal = Column(String(20), nullable=False)
    rua = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100), nullable=False)
    cep = Column(String(8), nullable=False)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    ativo = Column(Integer, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'razao_social': self.razao_social,
            'cnpj': self.cnpj,
            'inscr_estadual': self.inscr_estadual,
            'inscr_municipal': self.inscr_municipal,
            'rua': self.rua,
            'numero': self.numero,
            'complemento': self.complemento,
            'cep': self.cep,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by,
            'ativo': self.ativo
        }

class MeusTelefones(db.Model):
    __tablename__ = 'meus_telefones'
    
    id = Column(Integer, primary_key=True)
    id_minha_empresa = Column(Integer, db.ForeignKey('minha_empresa.id'), nullable=False)
    telefone = Column(String(11), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, db.ForeignKey('usuarios.id'), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, db.ForeignKey('usuarios.id'), nullable=True)
    ativo = Column(Integer, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_minha_empresa': self.id_minha_empresa,
            'telefone': self.telefone,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by,
            'ativo': self.ativo
        }

class MeusEmails(db.Model):
    __tablename__ = 'meus_emails'
    
    id = Column(Integer, primary_key=True)
    id_minha_empresa = Column(Integer, db.ForeignKey('minha_empresa.id'), nullable=False)
    email = Column(String(100), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, db.ForeignKey('usuarios.id'), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, db.ForeignKey('usuarios.id'), nullable=True)
    ativo = Column(Integer, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_minha_empresa': self.id_minha_empresa,
            'email': self.email,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by,
            'ativo': self.ativo
        }

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    tipo_cliente = Column(Integer, nullable=False)
    razao_social = Column(String(100), nullable=True)
    cnpj = Column(String(14), nullable=True)
    inscr_estadual = Column(String(20), nullable=True)
    inscr_municipal = Column(String(20), nullable=True)   
    cpf = Column(String(11), nullable=True)
    ativo = Column(Integer, default=1, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    update_by = Column(Integer, nullable=True)    
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo_cliente': self.tipo_cliente,
            'razao_social': self.razao_social,
            'cnpj': self.cnpj,
            'inscr_estadual': self.inscr_estadual,
            'inscr_municipal': self.inscr_municipal,
            'cpf': self.cpf,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.update_by
        }

class Telefone(db.Model):
    __tablename__ = 'telefones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(Integer, nullable=False)
    ativo = Column(Integer, default=1, nullable=False)
    telefone = Column(String(20), nullable=False) 
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    update_by = Column(Integer, nullable=True)    
           
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'telefone': self.telefone,
            'tipo': self.tipo,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'ativo': self.ativo
        }

class Email(db.Model):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(Integer, nullable=False)
    ativo = Column(Integer, default=1, nullable=False)
    email = Column(String(100), nullable=False)    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    update_by = Column(Integer, nullable=True)    
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'email': self.email,
            'tipo': self.tipo,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'ativo': self.ativo
        }
        
class Endereco(db.Model):
    __tablename__ = 'endereco'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(Integer, nullable=False)
    rua = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    numero = Column(String(30), nullable=False)
    cidade = Column(String(255), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(8), nullable=False)
    complemento = Column(String(255), nullable=True)
    ativo = Column(Integer, default=1, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    update_by = Column(Integer, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'rua': self.rua,
            'bairro': self.bairro,
            'numero': self.numero,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'complemento': self.complemento,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by
        }
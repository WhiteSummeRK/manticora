from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Integer,
    String,
    LargeBinary,
    Date,
    Float,
    Boolean,
    ForeignKey,
    UniqueConstraint)
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

db_url = 'postgresql://manticora:manticora123@localhost:5432/manticora_db'
db = SQLAlchemy(app)


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    senha = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    bairro = Column(String(30), nullable=False)
    cidade = Column(String(30), nullable=False)
    rua = Column(String(100), nullable=False)
    numero = Column(String(5), nullable=True)
    complemento = Column(String(30), nullable=False)

    def __repr__(self):
        return """
        Cliente(nome={}, senha={}, email={}, bairro={},
        cidade={}, rua={}, numero={}, complemento={})
        """.format(self.nome, self.senha, self.email, self.bairro, self.cidade,
                   self.rua, self.numero, self.complemento)


class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    senha = Column(String(20), nullable=False)
    telefone = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    bairro = Column(String(30), nullable=False)
    cidade = Column(String(30), nullable=False)
    rua = Column(String(100), nullable=False)
    numero = Column(String(5), nullable=False)
    complemento = Column(String(30), nullable=True)
    imagem = Column(LargeBinary, nullable=False)

    def __repr__(self):
        return """
        Restaurante(nome={}, senha={}, bairro={}, email={}
        cidade={}, rua={}, numero={}, complemento={}, imagem={})
        """.format(self.nome, self.senha, self.email, self.bairro, self.cidade,
                   self.rua, self.numero, self.complemento, self.imagem)


class ClienteConta(db.Model):
    __tablename__ = "cliente_conta"

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id'))
    id_restaurante = Column(Integer, ForeignKey('restaurante.id'))
    cliente = relationship('Cliente')
    restaurante = relationship('Restaurante')
    conta = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return """ClienteConta(cliente={}, restaurante={}, conta={}, status={})
        """.format(self.cliente, self.restaurante, self.conta, self.status)


class Extrato(db.Model):
    __tablename__ = "extrato"

    id = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey('cliente_conta.id'))
    conta = relationship('ClienteConta')
    nome_item = Column(String(40), nullable=False)
    data = Column(DateTime, nullable=False, default=datetime.now())
    valor = Column(Float, nullable=False)

    def __repr__(self):
        return f"Extrato(conta={self.conta}, nome_item={self.nome_item}, \
        data={self.data}, valor={self.valor})"

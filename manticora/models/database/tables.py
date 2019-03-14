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

# db_url = 'postgresql://manticora:manticora123@localhost:5432/manticora_db'
db_url = 'postgres://tcjktyoqzsmxdg:476db29152bf604203e8cf71007ffce69c574c8f98b7dfde2f356b11b7f04dee@ec2-75-101-131-79.compute-1.amazonaws.com:5432/dfa118jlcsd94c'
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    senha = Column(String(20), nullable=False)
    email = Column(String(50), nullable=True)
    bairro = Column(String(30), nullable=True)
    cidade = Column(String(30), nullable=True)
    rua = Column(String(100), nullable=True)
    numero = Column(String(5), nullable=True)
    complemento = Column(String(30), nullable=True)
    is_adm = Column(Boolean, default=False, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not is_authenticated()

    def get_id(self):
        return chr(self.id)

    def __repr__(self):
        return """
        Usuario(nome={}, senha={}, email={}, bairro={},
        cidade={}, rua={}, numero={}, complemento={}, is_adm={})
        """.format(self.nome, self.senha, self.email, self.bairro, self.cidade,
                   self.rua, self.numero, self.complemento, self.is_adm)


class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = Column(Integer, primary_key=True)
    telefone = Column(String(11), nullable=False)
    imagem = Column(LargeBinary, nullable=False)
    id_adm = Column(Integer, ForeignKey('usuario.id'))
    adm = relationship('Usuario')


class UsuarioConta(db.Model):
    __tablename__ = "usuario_conta"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    id_restaurante = Column(Integer, ForeignKey('restaurante.id'))
    usuario = relationship('Usuario')
    restaurante = relationship('Restaurante')
    conta = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return """UsuarioConta(usuario={}, restaurante={}, conta={}, status={})
        """.format(self.usuario, self.restaurante, self.conta, self.status)


class Extrato(db.Model):
    __tablename__ = "extrato"

    id = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey('usuario_conta.id'))
    conta = relationship('UsuarioConta')
    nome_item = Column(String(40), nullable=False)
    data = Column(DateTime, nullable=False, default=datetime.now())
    valor = Column(Float, nullable=False)

    def __repr__(self):
        return f"Extrato(conta={self.conta}, nome_item={self.nome_item}, \
        data={self.data}, valor={self.valor})"

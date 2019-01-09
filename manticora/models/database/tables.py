from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    UniqueConstraint)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

db_url = 'postgresql://manticora:manticora123@localhost:5432/manticora_db'
db = SQLAlchemy(app)


class Account(db.Model):
    __tablename__ = 'Account'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    pwd = Column(String(20), nullable=False)
    bill = Column(Float, nullable=False, default=0)
    is_adm = Column(Boolean, nullable=False)
    email = Column(String(100) nullable=False)
    neighborhood = Column(String(60), nullable=False)
    number = Column(String(6), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(2), nullable=False)
    complement = Column(String(100), nullable=True)

    def __repr__(self):
        return """
        Account(name={}, pwd={}, bill={}, is_adm={}, email={}, neighborhood={}, number={}
        city={}, state={}, complement={})
        """.format(self.name, self.pwd, self.bill, self.is_adm, self.email,
                   self.neighborhood, self.number, self.city, self.state, self.complement)

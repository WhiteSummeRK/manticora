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
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    pwd = Column(String(20), nullable=False)
    bill = Column(Float, nullable=False, default=0)

    def __repr__(self):
        return f'User(name={self.name}, pwd={self.pwd}, bill={self.bill})'

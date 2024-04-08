from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Planet(Base):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    diameter = Column(Integer, nullable=True)
    population =  Column(Integer, nullable=True)

    def __repr__(self):
        return f"Planet(name={self.name}, diameter={self.diameter}, population={self.population})"
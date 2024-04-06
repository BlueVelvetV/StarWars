from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Planet(Base):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    diameter = Column(Integer)
    climate = Column(String)
    terrain = Column(String)
    population = Column(Integer)
    residents = Column(JSON)

    def __repr__(self):
        return f'<Planet {self.name}>'

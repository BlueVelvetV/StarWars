from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String, nullable=False)
    terrain = db.Column(db.String, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    residents = db.Column(db.JSON)

    def __repr__(self):
        return f'<Planet {self.name}>'


"""from flask_sqlalchemy.model import Model

class Planet(Model):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    diameter = Column(Integer, nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    population = Column(Integer, nullable=False)
    residents = Column(JSON)

    def __repr__(self):
        return f'<Planet {self.name}>'
"""

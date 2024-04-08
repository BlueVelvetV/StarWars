from flask import g
# class Planet(Base):
#     __tablename__ = 'planets'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     diameter = Column(Integer, nullable=True)
#     population =  Column(Integer, nullable=True)
#
#     def __repr__(self):
#         return f"Planet(name={self.name}, diameter={self.diameter}, population={self.population})"
#
#

db = g.db
# Define the SQLAlchemy model for the 'planets' table
class Planet(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population
        }

class Climate(db.Model):
    __tablename__ = 'climates'

    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String)


class Terrain(db.Model):
    __tablename__ = 'terrains'

    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String)

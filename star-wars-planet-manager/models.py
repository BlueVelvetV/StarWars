import requests
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

def fetch_planets():
    graphql_query = """
    query {
        allPlanets {
          planets {
            name
            diameter
            climates
            terrains
            population
          }
        }
    }
    """
    response = requests.post('https://swapi-graphql.netlify.app/.netlify/functions/index', json={'query': graphql_query})
    if response.status_code == 200:
        data = response.json()['data']['allPlanets']['planets']
        return data
    else:
        return None

# Assuming you have initialized your SQLAlchemy session as `db_session`
planets_data = fetch_planets()
if planets_data:
    for planet_data in planets_data:
        new_planet = Planet(
            name=planet_data['name'],
            diameter=planet_data['diameter'],
            climate=planet_data['climate'],
            terrain=planet_data['terrain'],
            population=planet_data['population']
        )
        db_session.add(new_planet)
    db_session.commit()
else:
    print("Failed to fetch planets from the API.")

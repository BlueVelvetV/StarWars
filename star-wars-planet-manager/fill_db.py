import requests
from flask_sqlalchemy import SQLAlchemy
from models import Planet


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
    response = requests.post('https://swapi-graphql.netlify.app/.netlify/functions/index',
                             json={'query': graphql_query})
    if response.status_code == 200:
        data = response.json()['data']['allPlanets']['planets']
        return data
    else:
        return None


def populate_database(db: SQLAlchemy):
    db.create_all() # TODO :
    planets_data = fetch_planets()
    db_session = db.session

    if planets_data:
        for planet_data in planets_data:
            new_planet = Planet(
                name=planet_data['name'],
                diameter=planet_data['diameter'],
                climate=planet_data['climates'][0],  # TODO: could be more than 1
                terrain=planet_data['terrains'][0],
                population=planet_data['population']
            )
            db_session.add(new_planet)
        db_session.commit()
    else:
        print("Failed to fetch planets from the API.")

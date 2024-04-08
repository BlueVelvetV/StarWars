import requests
from flask_sqlalchemy import SQLAlchemy
from models import Planet
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
        #print('Response :', response.json())
        data = response.json()['data']['allPlanets']['planets']
        return data
    else:
        return None


def populate_database(db: SQLAlchemy,session: sessionmaker):
    planets_data = fetch_planets()
    print('PLANETS_DATA: ', planets_data)

    if planets_data:
        for planet_data in planets_data:
            #print('FIRST ITEM' , planet_data['name'])
            new_planet = Planet(
                name=planet_data['name'],
                diameter=planet_data['diameter'],
                population=planet_data['population']
            )
            print('NEW PLANET: ', new_planet)
            session.add(new_planet)
            session.commit() 
    else:
        print("Failed to fetch planets from the API.")

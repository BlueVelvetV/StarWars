import requests
from models import Planet, Climate, Terrain


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
        # print('Response :', response.json())
        data = response.json()['data']['allPlanets']['planets']
        return data
    else:
        return None


def populate_database(db):
    session = db.session

    def climate_fun(name, climate):
        new_climate = Climate(
            planet_name=name,
            name=climate
        )
        session.add(new_climate)

    def terrain_fun(name, terrain):
        new_terrain = Terrain(
            planet_name=name,
            name=terrain
        )
        session.add(new_terrain)

    planets_data = fetch_planets()

    if planets_data:
        for planet_data in planets_data:
            new_planet = Planet(
                name=planet_data['name'],
                diameter=planet_data['diameter'],
                population=planet_data['population']
            )
            session.add(new_planet)

            climates = planet_data['climates']
            [climate_fun(planet_data['name'], x) for x in climates]
            terrains = planet_data['terrains']
            [terrain_fun(planet_data['name'], x) for x in terrains]

            session.commit()
    else:
        print("Failed to fetch planets from the API.")

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import select

DATABASE_URL = 'sqlite:///planets.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

# Configure SQLAlchemy engine

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    #db.session.execute(select(Planet)).all()

    planet_dict = []
    for pl in planets:
        pl_dict=pl.__dict__
        pl_dict.pop('_sa_instance_state', None)
        planet_dict.append(pl_dict)

    print(planet_dict)
    return jsonify(planet_dict)


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        planet_data = {
            'id': planet.id,
            'name': planet.name,
            'diameter': planet.diameter,
            'climates': planet.climates,
            'terrains': planet.terrains,
            'population': planet.population,
            'residents': []
        }

        # Fetch residents from Star Wars API
        for resident_url in planet.residents:
            resident_response = requests.get(resident_url)
            if resident_response.status_code == 200:
                resident_data = resident_response.json()
                planet_data['residents'].append({
                    'name': resident_data['name'],
                    'height': resident_data['height'],
                    'gender': resident_data['gender']
                })

        return jsonify(planet_data)
    else:
        return jsonify({'message': 'Planet not found'}), 404

@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(
        name=data['name'],
        diameter=data['diameter'],
        climates=data['climates'],
        terrains=data['terrains'],
        population=data['population']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'message': 'Planet added successfully'}), 201


@app.route('/planet/<int:planet_id>', methods=['PUT'])
def edit_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        data = request.json
        planet.name = data.get('name', planet.name)
        planet.diameter = data.get('diameter', planet.diameter)
        planet.climates = data.get('climates', planet.climates)
        planet.terrain = data.get('terrain', planet.terrain)
        planet.population = data.get('population', planet.population)
        db.session.commit()
        return jsonify({'message': 'Planet updated successfully'})
    else:
        return jsonify({'message': 'Planet not found'}), 404


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'Planet deleted successfully'})
    else:
        return jsonify({'message': 'Planet not found'}), 404


class Planet:
    pass


@app.route('/planets/search', methods=['GET'])
def search_planets():
    query = request.args.get('query')
    planets = Planet.query.filter(
        (Planet.name.ilike(f'%{query}%')) |
        (Planet.climates.ilike(f'%{query}%')) |
        (Planet.terrain.ilike(f'%{query}%'))
    ).all()
    if planets:
        output = []
        for planet in planets:
            planet_data = {'id': planet.id, 'name': planet.name, 'diameter': planet.diameter, 'climates': planet.climates,
                           'terrains': planet.terrain, 'population': planet.population}
            output.append(planet_data)
        return jsonify({'planets': output})
    else:
        return jsonify({'message': 'No planets found matching the search criteria'})





"""
def fetch_planets():
    graphql_query = "
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
        }"
    response = requests.post('https://swapi-graphql.netlify.app/.netlify/functions/index',
                            json={'query': graphql_query})
    if response.status_code == 200:
            #print('Response :', response.json())
            data = response.json()['data']['allPlanets']['planets']
            return data
    else:
            return None
            
def populate_database(session):
    planets_data = fetch_planets()
    #print('PLANETS_DATA: ', planets_data)
    
    if planets_data:
        for planet_data in planets_data:
            new_planet = Planet(
                name=planet_data['name'],
                diameter=planet_data['diameter'],
                population=planet_data['population']
            )
            print('Pianeta :', planet_data['name'])

            if len(planet_data['climates']) >= 1:
                print('ENTRA 1', planet_data['climates'][0])
                new_climate1 = Climate (
                    planet_name = planet_data['name'],
                    name = planet_data['climates'][0]
                ) 
                session.add(new_climate1)
            if len(planet_data['climates']) > 1:
                print('ENTRA 2', planet_data['climates'][1])
                new_climate2 = Climate (
                    planet_name = planet_data['name'],
                    name = planet_data['climates'][1]
                ) 
                session.add(new_climate2,)
            if len(planet_data['climates']) > 2:
                print('ENTRA 3', planet_data['climates'][2])
                new_climate3 = Climate (
                    planet_name = planet_data['name'],
                    name = planet_data['climates'][2]
                ) 
                session.add(new_climate3)

            #print('NEW PLANET: ', new_climate1)
            session.add(new_planet)
            session.commit() 
    else:
        print("Failed to fetch planets from the API.")
"""
with app.app_context():
    g.db = db
    # Create tables in the database
    from models import Planet, Climate, Terrain
    db.create_all()

    from fill_db import populate_database
    populate_database(db)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



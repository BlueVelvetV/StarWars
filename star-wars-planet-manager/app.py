from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from fill_db import populate_database
from models import Planet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planets.db'
db = SQLAlchemy(app)


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        planet_data = {
            'id': planet.id,
            'name': planet.name,
            'diameter': planet.diameter,
            'climate': planet.climate,
            'terrain': planet.terrain,
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


@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(
        name=data['name'],
        diameter=data['diameter'],
        climate=data['climate'],
        terrain=data['terrain'],
        population=data['population'],
        residents=[]  # Initialize residents as empty list
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
        planet.climate = data.get('climate', planet.climate)
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


@app.route('/planets/search', methods=['GET'])
def search_planets():
    query = request.args.get('query')
    planets = Planet.query.filter(
        (Planet.name.ilike(f'%{query}%')) |
        (Planet.climate.ilike(f'%{query}%')) |
        (Planet.terrain.ilike(f'%{query}%'))
    ).all()
    if planets:
        output = []
        for planet in planets:
            planet_data = {'id': planet.id, 'name': planet.name, 'diameter': planet.diameter, 'climate': planet.climate,
                           'terrain': planet.terrain, 'population': planet.population}
            output.append(planet_data)
        return jsonify({'planets': output})
    else:
        return jsonify({'message': 'No planets found matching the search criteria'})


with app.app_context():
    populate_database(db)

if __name__ == '__main__':
    app.run(debug=True)

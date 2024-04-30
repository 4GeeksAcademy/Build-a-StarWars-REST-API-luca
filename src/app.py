from flask import Flask, jsonify, request
from models import db, User, Character, Planet, Favorite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
db.init_app(app)

# Función para insertar datos iniciales en la base de datos
def insert_initial_data():
    with app.app_context():
        print("Insertando datos iniciales...")
        if User.query.count() == 0:
            # Inserta datos de usuarios
            user1 = User(username='user1', password='pass1', email='user1@example.com', address='123 Main St', phone='555-1234')
            db.session.add(user1)
            db.session.commit()
        if Character.query.count() == 0:
            # Inserta datos de personajes
            character1 = Character(name='Luke Skywalker', height='172', mass='77', hair_color='blond', skin_color='fair', eye_color='blue', birth_year='19BBY', gender='male', homeworld='Tatooine', species='Human', films=['A New Hope', 'The Empire Strikes Back', 'Return of the Jedi'], vehicles=['Snowspeeder', 'Imperial Speeder Bike'], starships=['X-wing', 'Imperial shuttle'])
            character2 = Character(name='Darth Vader', height='202', mass='136', hair_color='none', skin_color='white', eye_color='yellow', birth_year='41.9BBY', gender='male', homeworld='Tatooine', species='Human', films=['A New Hope', 'The Empire Strikes Back', 'Return of the Jedi', 'Revenge of the Sith'], vehicles=['TIE Advanced x1'], starships=['Executor'])
            db.session.add(character1)
            db.session.add(character2)
            db.session.commit()
        if Planet.query.count() == 0:
             # Inserta datos de planetas
            planet1 = Planet(name='Tatooine', rotation_period='23', orbital_period='304', diameter='10465', climate='arid', gravity='1 standard', terrain='desert', surface_water='1', population='200000')
            planet2 = Planet(name='Alderaan', rotation_period='24', orbital_period='364', diameter='12500', climate='temperate', gravity='1 standard', terrain='grasslands, mountains', surface_water='40', population='2000000000')
            db.session.add(planet1)
            db.session.add(planet2)
            db.session.commit()
        else:
            print("La tabla de usuarios no está vacía. No se insertarán datos iniciales.")

# Inserta datos iniciales en la base de datos cuando se inicie la aplicación
insert_initial_data()

# Vaciar la tabla de usuarios
def empty_user_table():
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

# Vaciar la tabla de personajes
def empty_character_table():
    with app.app_context():
        db.session.query(Character).delete()
        db.session.commit()

# Vaciar la tabla de planetas
def empty_planet_table():
    with app.app_context():
        db.session.query(Planet).delete()
        db.session.commit()

# Vaciar la tabla de favoritos
def empty_favorite_table():
    with app.app_context():
        db.session.query(Favorite).delete()
        db.session.commit()


@app.route('/empty',methods=['DELETE'])
def empty_tables():
    empty_user_table()
    empty_character_table()
    empty_planet_table()
    empty_favorite_table()
    return jsonify({'message': 'Base de datos vaciada'})

######################################## Users #################################
# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_user = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'address': user.address,
            'phone': user.phone
        }
        serialized_users.append(serialized_user)
    return jsonify(serialized_users)

# Ruta para obtener un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')

    user = User(username=username, password=password, email=email, address=address, phone=phone)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado correctamente'}), 201

# Ruta para obtener todos los favoritos de un usuario
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Obtén todos los favoritos asociados a este usuario
    user_favorites = user.favorites

    # Inicializa listas para almacenar personajes y planetas
    characters = []
    planets = []

    # Itera sobre los favoritos del usuario y clasifícalos en personajes y planetas
    for favorite in user_favorites:
        if favorite.character:
            characters.append({
                'id': favorite.character.id,
                'name': favorite.character.name,
                'height': favorite.character.height,
                'mass': favorite.character.mass,
                'hair_color': favorite.character.hair_color,
                'skin_color': favorite.character.skin_color,
                'eye_color': favorite.character.eye_color,
                'birth_year': favorite.character.birth_year,
                'gender': favorite.character.gender,
                'homeworld': favorite.character.homeworld,
                'species': favorite.character.species,
                'films': favorite.character.films,
                'vehicles': favorite.character.vehicles,
                'starships': favorite.character.starships
                
            })
        elif favorite.planet:
            planets.append({
                'id': favorite.planet.id,
                'name': favorite.planet.name,
                'rotation_period': favorite.planet.rotation_period,
                'orbital_period': favorite.planet.orbital_period,
                'diameter': favorite.planet.diameter,
                'climate': favorite.planet.climate,
                'gravity': favorite.planet.gravity,
                'terrain': favorite.planet.terrain,
                'surface_water': favorite.planet.surface_water,
                'population': favorite.planet.population
                
            })

    # Retorna un JSON con las listas de personajes y planetas
    return jsonify({'characters': characters, 'planets': planets})

# Ruta para agregar un planeta favorito al usuario actual
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    
    user_id = request.args.get('user_id')

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Verifica si el planeta ya es un favorito del usuario
    existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({'message': 'El planeta ya está en favoritos'}), 400

    # Crea un nuevo registro de favorito para el planeta y guárdalo en la base de datos
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'El planeta se agregó a favoritos correctamente'}), 201

# Ruta para agregar un personaje favorito al usuario actual
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    
    user_id = request.args.get('user_id')

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Verifica si el personaje ya es un favorito del usuario
    existing_favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing_favorite:
        return jsonify({'message': 'Personaje ya está en favoritos'}), 400

    # Crea un nuevo registro de favorito para el personaje y guárdalo en la base de datos
    new_favorite = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Personaje agregado a favoritos correctamente'}), 201


# Ruta para eliminar un planeta de los favoritos del usuario actual
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet_favorite(planet_id):
    
    user_id = request.args.get('user_id')

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Busca el favorito del usuario asociado al planeta especificado
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'message': 'Planeta no encontrado favoritos del usuario'}), 404

    # Elimina el favorito del usuario de la base de datos
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Planeta eliminado de favoritos correctamente'}), 200

# Ruta para eliminar un personaje de los favoritos del usuario actual
@app.route('/favorite/people/<int:character_id>', methods=['DELETE'])
def remove_character_favorite(character_id):
    
    user_id = request.args.get('user_id')

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Busca el favorito del usuario asociado al personaje especificado
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({'message': 'Personaje no encontrado en favoritos del usuario'}), 404

    # Elimina el favorito del usuario de la base de datos
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Personaje eliminado de favoritos correctamente'}), 200

########################## Characteres ################################


@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    serialized_characters = []
    for character in characters:
        serialized_character = {
            'id': character.id,
            'name': character.name,
            'height': character.height,
            'mass': character.mass,
            'hair_color': character.hair_color,
            'skin_color': character.skin_color,
            'eye_color': character.eye_color,
            'birth_year': character.birth_year,
            'gender': character.gender,
            'homeworld': character.homeworld,
            'species': character.species,
            'films': character.films,
            'vehicles': character.vehicles,
            'starships': character.starships
            
        }
        serialized_characters.append(serialized_character)
    return jsonify(serialized_characters)

# Ruta para obtener un personaje por su ID
@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character:
        serialized_character = {
            'id': character.id,
            'name': character.name,
            'height': character.height,
            'mass': character.mass,
            'hair_color': character.hair_color,
            'skin_color': character.skin_color,
            'eye_color': character.eye_color,
            'birth_year': character.birth_year,
            'gender': character.gender,
            'homeworld': character.homeworld,
            'species': character.species,
            'films': character.films,
            'vehicles': character.vehicles,
            'starships': character.starships
            
        }
        return jsonify(serialized_character)
    else:
        return jsonify({'message': 'Personaje no encontrado'}), 404
    
# Ruta para agregar un nuevo personaje
@app.route('/people', methods=['POST'])
def add_character():
    data = request.json
    new_character = Character(
        name=data.get('name'),
        height=data.get('height'),
        mass=data.get('mass'),
        hair_color=data.get('hair_color'),
        skin_color=data.get('skin_color'),
        eye_color=data.get('eye_color'),
        birth_year=data.get('birth_year'),
        gender=data.get('gender'),
        homeworld=data.get('homeworld'),
        species=data.get('species'),
        films=data.get('films'),
        vehicles=data.get('vehicles'),
        starships=data.get('starships')
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'message': 'Personaje agregado correctamente'}), 201

# Ruta para actualizar un personaje existente
@app.route('/people/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Personaje no encontrado'}), 404

    data = request.json
    character.name = data.get('name', character.name)
    character.height = data.get('height', character.height)
    character.mass = data.get('mass', character.mass)
    character.hair_color = data.get('hair_color', character.hair_color)
    character.skin_color = data.get('skin_color', character.skin_color)
    character.eye_color = data.get('eye_color', character.eye_color)
    character.birth_year = data.get('birth_year', character.birth_year)
    character.gender = data.get('gender', character.gender)
    character.homeworld = data.get('homeworld', character.homeworld)
    character.species = data.get('species', character.species)
    character.films = data.get('films', character.films)
    character.vehicles = data.get('vehicles', character.vehicles)
    character.starships = data.get('starships', character.starships)

    db.session.commit()
    return jsonify({'message': 'Personaje actualizado correctamente'}), 200

# Ruta para eliminar un personaje
@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Personaje no encontrado'}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Personaje eliminado correctamente'}), 200

########################## Planets ################################

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = []
    for planet in planets:
        serialized_planet = {
            'id': planet.id,
            'name': planet.name,
            'rotation_period': planet.rotation_period,
            'orbital_period': planet.orbital_period,
            'diameter': planet.diameter,
            'climate': planet.climate,
            'gravity': planet.gravity,
            'terrain': planet.terrain,
            'surface_water': planet.surface_water,
            'population': planet.population
            
        }
        serialized_planets.append(serialized_planet)
    return jsonify(serialized_planets)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        serialized_planet = {
            'id': planet.id,
            'name': planet.name,
            'rotation_period': planet.rotation_period,
            'orbital_period': planet.orbital_period,
            'diameter': planet.diameter,
            'climate': planet.climate,
            'gravity': planet.gravity,
            'terrain': planet.terrain,
            'surface_water': planet.surface_water,
            'population': planet.population
            
        }
        return jsonify(serialized_planet)
    else:
        return jsonify({'message': 'Planeta no encontrado'}), 404

# Ruta para agregar un nuevo planeta
@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(
        name=data.get('name'),
        rotation_period=data.get('rotation_period'),
        orbital_period=data.get('orbital_period'),
        diameter=data.get('diameter'),
        climate=data.get('climate'),
        gravity=data.get('gravity'),
        terrain=data.get('terrain'),
        surface_water=data.get('surface_water'),
        population=data.get('population')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'message': 'Planeta agregado correctamente'}), 201

# Ruta para actualizar un planeta existente
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planeta no encontrado'}), 404

    data = request.json
    planet.name = data.get('name', planet.name)
    planet.rotation_period = data.get('rotation_period', planet.rotation_period)
    planet.orbital_period = data.get('orbital_period', planet.orbital_period)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.climate = data.get('climate', planet.climate)
    planet.gravity = data.get('gravity', planet.gravity)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.surface_water = data.get('surface_water', planet.surface_water)
    planet.population = data.get('population', planet.population)

    db.session.commit()
    return jsonify({'message': 'Planeta actualizado correctamente'}), 200

# Ruta para eliminar un planeta
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planeta no encontrado'}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({'message': 'Planeta eliminado correctamente'}), 200


if __name__ == '__main__':
    # Crea las tablas en la base de datos
    with app.app_context():
        db.create_all()
    app.run(debug=True)

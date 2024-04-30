from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    favorites = db.relationship('Favorite', backref='user')

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(10), nullable=True)
    mass = db.Column(db.String(10), nullable=True)
    hair_color = db.Column(db.String(50), nullable=True)
    skin_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    birth_year = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    homeworld = db.Column(db.String(100), nullable=True)
    species = db.Column(db.String(100), nullable=True)
    films = db.Column(db.JSON, nullable=True)
    vehicles = db.Column(db.JSON, nullable=True)
    starships = db.Column(db.JSON, nullable=True)
    favorites = db.relationship('Favorite', backref='character')

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.String(10), nullable=True)
    orbital_period = db.Column(db.String(10), nullable=True)
    diameter = db.Column(db.String(20), nullable=True)
    climate = db.Column(db.String(100), nullable=True)
    gravity = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    surface_water = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    favorites = db.relationship('Favorite', backref='planet')

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

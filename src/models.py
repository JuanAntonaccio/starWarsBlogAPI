from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos_per = db.relationship('Favorito_perso', backref='usuario', lazy=True)
    favoritos_plane = db.relationship('Favorito_plane', backref='usuario', lazy=True)
    # esto es similiar al toString en Java
    def __repr__(self):
        return '<Usuario %r %r>' % (self.name, self.email)
    # esto deberian tener todas las tablas a crear este metodo
    # que devuelve un diccionario

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }




class Favorito_perso(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    perso_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "perso_id": self.perso_id
        }

class Favorito_plane(db.Model):
    #__tablename__ = 'favoritos_plane'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    plane_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "plane_id": self.plane_id
        }

class Personaje(db.Model):
    #__tablename__='personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(50), nullable=False)
    mass = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    usuarios = db.relationship('Favorito_perso', backref='personaje', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "skin_color":self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }

class Planeta(db.Model):
    #__tablename__='planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rotation_period = db.Column(db.String(50), nullable=False)
    orbital_period = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    surface_water = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)  
    usuarios = db.relationship('Favorito_plane', backref='planeta', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter":self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain":self.terrain,
            "surface_water": self.surface_water,
            "population": self.population

        }      
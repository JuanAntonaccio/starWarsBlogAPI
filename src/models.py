from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # esto es similiar al toString en Java
    def __repr__(self):
        return '<Usarios %r %r>' % (self.name, self.email)
    # esto deberian tener todas las tablas a crear este metodo
    # que devuelve un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }




class Favorito_perso(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    perso_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    

    def serialize(self):
        return {}

class Favorito_plane(db.Model):
    #__tablename__ = 'favoritos_plane'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    plane_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    def serialize(self):
        return {}

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
    def serialize(self):
        return {}

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
    def serialize(self):
        return {}      
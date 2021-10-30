"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Favorito_perso,Favorito_plane,Planeta,Personaje
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():

    usuarios=Usuario.query.all()
    usuarios = list(map(lambda usuario: usuario.serialize(), usuarios ))
    if not usuarios:
        return jsonify("no se encontraron usuarios"),404
        
    return jsonify(usuarios), 200

@app.route('/personajes', methods=['GET'])
def get_all_personajes():

    personajes=Personaje.query.all()
    personajes = list(map(lambda per: per.serialize(), personajes ))
    if not personajes:
        return jsonify("no se encontraron personajes"),404
        
    return jsonify(personajes), 200    

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personaje(id):

    personajes=(Personaje.query.get(id)).serialize()
    #personajes = list(map(lambda per: per.serialize(), personajes ))
    if not personajes:
        return jsonify("no se encontro al personaje"),404
        
    return jsonify(personajes), 200 


@app.route('/personajes', methods=['POST'])
def add_personaje():
    # primero leo lo que viene en el body
    body_personaje=json.loads(request.data)
    #print (body_personaje)
    persona=Personaje(name=body_personaje['name'],height=body_personaje['height'],mass=body_personaje['mass'],hair_color=body_personaje['hair_color'],skin_color=body_personaje['skin_color'],eye_color=body_personaje['eye_color'],birth_year=body_personaje['birth_year'])
    
    
    db.session.add(persona)               
    db.session.commit()
    
    personajes=Personaje.query.all()
    personajes = list(map(lambda per: per.serialize(), personajes ))
    if not personajes:
        return jsonify("no se encontraron personajes"),404
        
    return jsonify(personajes), 200  
    

    



@app.route('/personajes/<int:id>', methods=['PUT'])
def update_personaje(id):
    body=json.loads(request.data)
    personaje=Personaje.query.get(id)
    if personaje is None:
        raise APIException('Personaje no encontrado',status_code=404)
    if "name" in body:
        personaje.name=body['name']
    if "height" in body:
        personaje.height=body['height']  
    if "mass" in body:
        personaje.mass=body['mass']
    if "hair_color" in body:
        personaje.hair_color=body['hair_color'] 
    if "skin_color" in body:
        personaje.skin_color=body['skin_color']    
    if "eye_color" in body:
        personaje.eye_color=body['eye_color']    
    if "birth_year" in body:
        personaje.birth_year=body['birth_year']                 
    db.session.commit()
    personajes=Personaje.query.all()
    personajes = list(map(lambda per: per.serialize(), personajes ))
    if not personajes:
        return jsonify("no se encontraron personajes"),404
        
    return jsonify(personajes), 200  


@app.route('/personajes/<int:id>', methods=['DELETE'])
def delete_personaje(id):
    
    personaje=Personaje.query.get(id)
    if personaje is None:
        raise APIException('Personaje no encontrado',status_code=404)
    db.session.delete(personaje)                
    db.session.commit()
    personajes=Personaje.query.all()
    personajes = list(map(lambda per: per.serialize(), personajes ))
    if not personajes:
        return jsonify("no se encontraron personajes"),404
        
    return jsonify(personajes), 200  


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

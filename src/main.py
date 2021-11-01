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

#-----------------------------------------------------------
# Endpoints de usuarios
#-----------------------------------------------------------

@app.route('/usuarios', methods=['GET'])
def get_all_users():

    usuarios=Usuario.query.all()
    usuarios = list(map(lambda usuario: usuario.serialize(), usuarios ))
    if not usuarios:
        return jsonify("no se encontraron usuarios"),404
        
    return jsonify(usuarios), 200

@app.route('/usuarios', methods=['POST'])
def add_user():
    # primero leo lo que viene en el body
    body_us=json.loads(request.data)
    #print (body_us)
    usuario=Usuario(name=body_us['name'],email=body_us['email'],password=body_us['password'],is_active=body_us['is_active'])
    db.session.add(usuario)               
    db.session.commit()
    
    

    usuarios=Usuario.query.all()
    usuarios = list(map(lambda usuario: usuario.serialize(), usuarios ))
    if not usuarios:
        return jsonify("no se encontraron usuarios"),404
        
    return jsonify(usuarios), 200


@app.route('/usuarios/favoritos/<int:id>', methods=['GET'])
def get_all_users_favoritos(id):
    favoritos={}

    usu_per=Favorito_perso.query.filter_by(usuario_id=id)
    usu_plan=Favorito_plane.query.filter_by(usuario_id=id)
    usu_per=list(map(lambda favoritos_per: favoritos_per.serialize(), usu_per))
    usu_plan=list(map(lambda favoritos_plane: favoritos_plane.serialize(), usu_plan))
    #usuarios={"personajes":usu_per,
    #          "planetas":usu_pan}
    #usuario2=json.dumps(usuarios)
    favoritos['personajes']=usu_per
    favoritos['planetas']=usu_plan
    if not favoritos:
        return jsonify("no se encontraron usuarios"),404
        
    return jsonify(favoritos), 200


#-----------------------------------------------
# EndPoints de Favoritos Personajes
# ----------------------------------------------   
@app.route('/favoritosPersonajes', methods=['POST'])
def add_fav_per():
    # primero leo lo que viene en el body
    body_fav=json.loads(request.data)
    #print (body_fav)
    esta1=False
    esta2=False
    if "perso_id" in body_fav:
        personaje=Personaje.query.get(body_fav['perso_id'])
        if personaje is None:
            raise APIException('Personaje no encontrado',status_code=404)
        else:
            esta1=True
    if "usuario_id" in body_fav:    
        usuario=Usuario.query.get(body_fav['usuario_id'])
        if usuario is None:
            raise APIException('Usuario no encontrado',status_code=404)
        else:
            esta2=True    
    esta=esta1 and esta2


    if esta:        
        preg=Favorito_perso.query.filter(Favorito_perso.usuario_id==body_fav['usuario_id'],Favorito_perso.perso_id==body_fav['perso_id']).first()
        if preg:
            raise APIException('Favorito Personaje repetido',status_code=404)
        favper=Favorito_perso(usuario_id=body_fav['usuario_id'],perso_id=body_fav['perso_id'])
        db.session.add(favper)               
        db.session.commit()
    
    

    favoritos=Favorito_perso.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos personajes"),404
        
    return jsonify(favoritos), 200

@app.route('/favoritosPersonajes', methods=['DELETE'])
def delete_fav_per():
    # primero leo lo que viene en el body
    body_fav=json.loads(request.data)
    #print (body_fav)
    esta1=False
    esta2=False
    if "perso_id" in body_fav:
        personaje=Personaje.query.get(body_fav['perso_id'])
        if personaje is None:
            raise APIException('Personaje no encontrado',status_code=404)
        else:
            esta1=True
    if "usuario_id" in body_fav:    
        usuario=Usuario.query.get(body_fav['usuario_id'])
        if usuario is None:
            raise APIException('Usuario no encontrado',status_code=404)
        else:
            esta2=True    
    esta=esta1 and esta2


    if esta:        
        favper=Favorito_perso.query.filter(Favorito_perso.usuario_id==body_fav['usuario_id'],Favorito_perso.perso_id==body_fav['perso_id']).first()
        if favper:
            db.session.delete(favper)             
            db.session.commit()
        else:
            raise APIException('Datos no encontrados en favoritos personajes',status_code=404)
        
    
    

    favoritos=Favorito_perso.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos personajes"),404
        
    return jsonify(favoritos), 200    

@app.route('/favoritosPersonajes', methods=['GET'])
def get_all_favper():

    favoritos=Favorito_perso.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos personajes"),404
        
    return jsonify(favoritos), 200

#-----------------------------------------------
# EndPoints de FavoritosPlanetas
#-----------------------------------------------

@app.route('/favoritosPlanetas', methods=['POST'])
def add_fav_pla():
    # primero leo lo que viene en el body
    body_fav=json.loads(request.data)
    #print (body_fav)
    esta1=False
    esta2=False
    if "plane_id" in body_fav:
        planeta=Planeta.query.get(body_fav['plane_id'])
        if planeta is None:
            raise APIException('Planeta no encontrado',status_code=404)
        else:
            esta1=True
    if "usuario_id" in body_fav:    
        usuario=Usuario.query.get(body_fav['usuario_id'])
        if usuario is None:
            raise APIException('Usuario no encontrado',status_code=404)
        else:
            esta2=True    
    esta=esta1 and esta2
    if esta:       
        preg=Favorito_plane.query.filter(Favorito_plane.usuario_id==body_fav['usuario_id'],Favorito_plane.plane_id==body_fav['plane_id']).first()
        if preg:
            raise APIException('Favorito Planeta repetido',status_code=404) 
        favpla=Favorito_plane(usuario_id=body_fav['usuario_id'],plane_id=body_fav['plane_id'])
        db.session.add(favpla)               
        db.session.commit()
    
    

    favoritos=Favorito_plane.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos planetas"),404
        
    return jsonify(favoritos), 200

@app.route('/favoritosPlanetas', methods=['GET'])
def get_all_favpla():

    favoritos=Favorito_plane.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos planetas"),404
        
    return jsonify(favoritos), 200


@app.route('/favoritosPlanetas', methods=['DELETE'])
def delete_fav_planeta():
    # primero leo lo que viene en el body
    body_fav=json.loads(request.data)
    #print (body_fav)
    esta1=False
    esta2=False
    if "plan_id" in body_fav:
        planeta=Planeta.query.get(body_fav['plane_id'])
        if planeta is None:
            raise APIException('Planeta no encontrado',status_code=404)
        else:
            esta1=True
    if "usuario_id" in body_fav:    
        usuario=Usuario.query.get(body_fav['usuario_id'])
        if usuario is None:
            raise APIException('Usuario no encontrado',status_code=404)
        else:
            esta2=True    
    esta=esta1 and esta2


    if esta:        
        favpla=Favorito_plane.query.filter(Favorito_plane.usuario_id==body_fav['usuario_id'],Favorito_plane.plane_id==body_fav['plane_id']).first()
        if favpla:
            db.session.delete(favpla)             
            db.session.commit()
        else:
            raise APIException('Datos no encontrados en favoritos planetas',status_code=404)
        
    
    

    favoritos=Favorito_plane.query.all()
    favoritos = list(map(lambda favo: favo.serialize(), favoritos ))
    if not favoritos:
        return jsonify("no se encontraron favoritos planetas"),404
        
    return jsonify(favoritos), 200    



#-------------------------------------------------
# EndPoints de Personajes
# -------------------------------------------    

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

#-------------------------------------------------
# EndPoints de Planetas
# -------------------------------------------    
#   

@app.route('/planetas', methods=['GET'])
def get_all_planetas():

    planetas=Planeta.query.all()
    planetas = list(map(lambda pla: pla.serialize(), planetas ))
    if not planetas:
        return jsonify("no se encontraron planetas"),404
        
    return jsonify(planetas), 200    

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta(id):

    planetas=(Planeta.query.get(id))
    if planetas != None:
        planetas=planetas.serialize()
    
    
    if not planetas:
        return jsonify("no se encontro al planeta"),404
    else:    
        return jsonify(planetas), 200 


@app.route('/planetas', methods=['POST'])
def add_planeta():
    # primero leo lo que viene en el body
    b_pl=json.loads(request.data)
    #print (b_pl)
    planeta=Planeta(name=b_pl['name'],rotation_period=b_pl['rotation_period'],orbital_period=b_pl['orbital_period'],diameter=b_pl['diameter'],climate=b_pl['climate'],gravity=b_pl['gravity'],terrain=b_pl['terrain'],surface_water=b_pl['surface_water'],population=b_pl['population'])
    
    
    db.session.add(planeta)               
    db.session.commit()
    
    planetas=Planeta.query.all()
    planetas = list(map(lambda plan: plan.serialize(), planetas ))
    if not planetas:
        return jsonify("no se encontraron planetas"),404
        
    return jsonify(planetas), 200  
    

    



@app.route('/planetas/<int:id>', methods=['PUT'])
def update_planeta(id):
    body=json.loads(request.data)
    planeta=Planeta.query.get(id)
    if planeta is None:
        raise APIException('Planeta no encontrado',status_code=404)
    if "name" in body:
        planeta.name=body['name']
    if "rotation_period" in body:
        planeta.rotation_period=body['rotation_period']  
    if "orbital_period" in body:
        planeta.orbital_period=body['orbital_period']
    if "diameter" in body:
        planeta.diameter=body['diameter'] 
    if "climate" in body:
        planeta.climate=body['climate']    
    if "gravity" in body:
        planeta.gravity=body['gravity']    
    if "terrain" in body:
        planeta.terrain=body['terrain']
    if "surface_water" in body:
        planeta.surface_water=body['surface_water']
    if "population" in body:
        planeta.population=body['population']
  

    db.session.commit()
    planetas=Planeta.query.all()
    planetas = list(map(lambda plan: plan.serialize(), planetas ))
    if not planetas:
        return jsonify("no se encontraron planetas"),404
        
    return jsonify(planetas), 200  


@app.route('/planetas/<int:id>', methods=['DELETE'])
def delete_planeta(id):
    
    planeta=Planeta.query.get(id)
    if planeta is None:
        raise APIException('Planeta no encontrado',status_code=404)
    db.session.delete(planeta)                
    db.session.commit()
    planetas=Planeta.query.all()
    planetas = list(map(lambda plan: plan.serialize(), planetas ))
    if not planetas:
        return jsonify("no se encontraron planetas"),404
        
    return jsonify(planetas), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
import datetime
#from models import Person

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app, resources={r"/*":{"origins":"*"}})
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():

    query = Personajes.query.all()
    results = list(map(lambda personaje: personaje.serialize(), query))

    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):

    query = Personajes.query.get(people_id)
    results = query.serialize()
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    query = Planetas.query.all()
    results = list(map(lambda planeta: planeta.serialize(), query))

    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):

    query = Planetas.query.get(planet_id)
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():

    query = User.query.all()
    results = list(map(lambda user: user.serialize(), query))

    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    query = Favoritos.query.filter_by(User_id=user_id)
    results = list(map(lambda favoritos: favoritos.serialize(), query))
    print(results)
    results2 = []
    
    for result in results:
        if result.get("planetas_id") == None:
            query_personajes = Personajes.query.get(result.get("personajes_id"))
            result["name"] = query_personajes.serialize().get("name")
            results2.append(result)
        else: 
            query_planetas = Planetas.query.get(result.get("planetas_id"))
            result["name"] = query_planetas.serialize().get("name")
            results2.append(result)

    response_body = {
        "message": results2
    }
    
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorito(user_id):

    request_favorito = request.get_json()
    print(request_favorito, "data")
    favo = Favoritos(User_id = user_id, planetas_id = request_favorito["planetas_id"], personajes_id = request_favorito["personajes_id"])
    db.session.add(favo)
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorito(favorite_id):

    del_favorito = Favoritos.query.get(favorite_id)
    if del_favorito is None:
        raise APIException('Favorito no encontrado', status_code=404)
    db.session.delete(del_favorito)
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/register', methods=["POST"])
def registro():
    if request.method == 'POST':
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not username:
            return jsonify({"message": " El usuario es requerido"}), 400
        if not email:
            return jsonify({"message": " El email es requerido"}), 400
        if not password:
            return jsonify({"message": "La contraseña es requerida"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"message": "Este nombre de usuario ya existe"}), 400

        user = User()
        user.email = email
        user.user = username
        hashed_password = generate_password_hash(password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"ok": "Gracias. se registro con exito", "status": "true"}), 200

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"message": "Nombre de usuario requerido"}), 400
        if not password:
            return jsonify({"message": "Contraseña requerida"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Nombre de usuario/contraseña son incorrectas"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"message": "Nombre de usuario/contraseña son incorrectas"}), 401

        expiracion = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.id, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

from app import app, ma, db, api
from models import User

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow  
from flask_restful import Api, Resource 

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import flask_praetorian
import flask_cors




jwt = JWTManager(app)
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()

guard.init_app(app, User)

@app.route('/members', methods=["GET"])
@jwt_required()
def members():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
    return {"members": ["member1","Member2","Member3"]}, 200


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    
    #req = request.get_json(force=True)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200
    """ username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username != "test" or password != "test" or username =='':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token) """


@app.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200

""" @app.route("/singUp", methods=["PUT"])
def singUp():
    
    new_user = User(
 
            
            mail = request.json['mail'],
            password = request.json['password'],
            roles = request.json['roles'],
            is_active = request.json['is_active']

        )
    db.session.add(new_user)

    db.session.commit()
    
    return user_schema.dump(new_user)
    return jsonify(mail = request.json['mail'],
            password = request.json['password'],
            roles = request.json['roles'],
            is_active = request.json['is_active']) """



class RecursoSingUp(Resource):
    def get(self, id_usuario):
        user = User.query.get_or_404(id_usuario)
        return User_schema.dump(user)
    
    def put(self):
        

        new_user = User(
 
            
            username = request.json['username'],
            password = guard.hash_password(request.json['password']),
            roles = request.json['roles'],
            is_active = request.json['is_active']

        )

        db.session.add(new_user)

        db.session.commit()

        return user_schema.dump(new_user)

api.add_resource(RecursoSingUp, '/singUp')

###############################################
###############################################3
#SCHEMAS 
class User_schema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password","roles", "is_active")

user_schema = User_schema()
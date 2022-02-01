from app import app
from models import *

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow  
from flask_restful import Api, Resource 

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



jwt = JWTManager(app)

@app.route('/members')
def members():
    return {"members": ["member1","Member2","Member3"]}


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test" or username =='':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
jwt = JWTManager(app)
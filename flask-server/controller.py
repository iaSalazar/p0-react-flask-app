from sqlalchemy import desc
from app import app, ma, db, api
from models import User, Event, user_schema, event_schema, events_schema

from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy 
#from flask_marshmallow import Marshmallow  
from flask_restful import Api, Resource 

#from flask_jwt_extended import create_access_token
#from flask_jwt_extended import get_jwt_identity
#from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import flask_praetorian
import flask_cors




jwt = JWTManager(app)
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()

guard.init_app(app, User)

@app.route('/members', methods=["GET"])
@flask_praetorian.auth_required
def members():
    # Access the identity of the current user with get_jwt_identity
    
    #return jsonify(logged_in_as=current_user), 200
    return jsonify(
        message="protected endpoint (allowed user {})".format(
            flask_praetorian.current_user().username,
        )
    )
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



@app.route("/singUp", methods=["PUT"])
def add_user():
    """
    add new user
    """
    new_user = User(
 
            
            username = request.json['username'],
            password = guard.hash_password(request.json['password']),
            roles = request.json['roles'],
            is_active = request.json['is_active']

        )

    db.session.add(new_user)

    db.session.commit()
    return user_schema.dump(new_user)

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    get user
    """
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)

@app.route("/events", methods=["PUT"])
@flask_praetorian.auth_required
def add_event():
    """
    add new event
    """
    new_event = Event(
 
            
            name = request.json['name'],
            description = request.json['description'],
            id_user = flask_praetorian.current_user().id

        )

    db.session.add(new_event)

    db.session.commit()
    
    return event_schema.dump(new_event)


@app.route("/events", methods=["GET"])
def get_all_event():
    """
    Get all events
    """
    event = Event.query.all()

    return jsonify(events_schema.dump(event))

@app.route("/events/<int:id_event>", methods=["GET"])
def get_event(id_event):
    """
    Get specific event
    """
   
    event = Event.query.get_or_404(id_event)

    

    return event_schema.dump(event)

@app.route("/events/<int:id_event>", methods=["DELETE"])
def delete_event(id_event):
    
   
    new_event = Event.query.get_or_404(id_event)

    db.session.delete(new_event)

    db.session.commit()

    return '', 204




# class ResourceOneEvent(Resource):


#     def get(self):

#         event = Event.query.all()

#         return event_schema.dump(event)
#     # def get(self, id_event):

#     #     event = Event.query.get_or_404(id_event)

#     #     return event_schema.dump(event)

#     def put(self):

#         new_event = Event(
 
            
#             name = request.json['name'],
#             description = request.json['description']

#         )
#         db.session.add(new_event)

#         db.session.commit()
    
#         return user_schema.dump(new_event)

#     def delete(self, id_event):

#         event = Event.query.get_or_404(id_event)

#         db.session.delete(event)

#         db.session.commit()

#         return '', 204
# api.add_resource(ResourceOneEvent, '/event')
#api.add_resource(ResourceOneEvent, '/event/<int:id_event>')
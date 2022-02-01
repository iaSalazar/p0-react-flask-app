from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow  
from flask_restful import Api, Resource 
from models import *

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"

db = SQLAlchemy(app) 

ma = Marshmallow(app)

api = Api(app)



# It must be done after declaring app
from controller import *

if __name__ == '__main__':
    app.run(debug=True)


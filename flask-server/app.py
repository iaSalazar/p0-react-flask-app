from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow  
from flask_restful import Api, Resource 




app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
app.secret_key = "super-secret"
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Setup the Flask-JWT-Extended extension



db = SQLAlchemy(app) 
ma = Marshmallow(app)

api = Api(app)


# It must be done after declaring app

from models import *
from controller import *

if __name__ == '__main__':
    app.run(debug=True)


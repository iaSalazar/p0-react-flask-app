from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from sqlalchemy import Integer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class User_schema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password","roles", "is_active")  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    description=db.Column(db.String(255))
    id_user=db.Column(Integer, db.ForeignKey(User.id))

class Event_schema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description","id_user")    


class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column( db.String(50) )
    contenido = db.Column( db.String(255) )
    
class Publicacion_Schema(ma.Schema):
    class Meta:
        fields = ("id", "titulo", "contenido")
    
post_schema = Publicacion_Schema()
posts_schema = Publicacion_Schema(many = True)
user_schema = User_schema()
event_schema = Event_schema()

class RecursoListarPublicaciones(Resource):
    def get(self):
        publicaciones = Publicacion.query.all()
        return posts_schema.dump(publicaciones)
    
    def post(self):
            nueva_publicacion = Publicacion(
                titulo = request.json['titulo'],
                contenido=request.json['contenido']
            )
            db.session.add(nueva_publicacion)
            db.session.commit()
            return post_schema.dump(nueva_publicacion)
     
class RecursoUnaPublicacion(Resource):
    def get(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        return post_schema.dump(publicacion)
    
    def put(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        if 'id' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'username' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'password' in request.json:
            publicacion.contenido = request.json['contenido']
        if 'is_active' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'roles' in request.json:
            publicacion.contenido = request.json['contenido']

        db.session.commit()
        return post_schema.dump(publicacion)

    def delete(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        db.session.delete(publicacion)
        db.session.commit()
        return '', 204


class RecursoSingUp(Resource):
    def get(self, id_usuario):
        publicacion = User.query.get_or_404(id_usuario)
        return post_schema.dump(publicacion)
    
    def put(self, id_usuario):
        publicacion = Publicacion.query.get_or_404(id_usuario)

        if 'titulo' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'contenido' in request.json:
            publicacion.contenido = request.json['contenido']

        db.session.commit()
        return post_schema.dump(publicacion)

    def delete(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        db.session.delete(publicacion)
        db.session.commit()
        return '', 204
api.add_resource(RecursoListarPublicaciones, '/publicaciones')     
api.add_resource(RecursoUnaPublicacion, '/publicaciones/<int:id_publicacion>')
api.add_resource(RecursoSingUp, '/singUp')     
api.add_resource(RecursoUnaPublicacion, '/publicaciones/<int:id_publicacion>')

if __name__ == '__main__':
    app.run(debug=True)
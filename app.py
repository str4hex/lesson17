from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

ns_movie = api.namespace('movies')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieScheme(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Integer()
    genre_id = fields.Integer()
    genre = fields.String()
    director_id = fields.String()
    director = fields.String()


@ns_movie.route("/")
class MovieViews(Resource):

    def get(self):
        movie_query = Movie.query.all()
        #movie_query = Movie.query.paginate(page=1, per_page=4, error_out=True)
        movie_scheme = MovieScheme(many=True)
        #return jsonify(movie_scheme.dump(movie_query.items))
        return jsonify(movie_scheme.dump(movie_query))


@ns_movie.route("/<int:uid>")
class MovieView(Resource):

    def get(self,uid):
        movie_query = Movie.query.get(uid)

        movie_scheme = MovieScheme()
        return jsonify(movie_scheme.dump(movie_query))


if __name__ == '__main__':
    app.run(debug=True)

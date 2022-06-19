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
ns_director = api.namespace('directors')
ns_genre = api.namespace('genres')


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
    director_name = fields.String()
    name_ganres = fields.String()


class DirectorScheme(Schema):
    id = fields.Integer()
    name = fields.String()


class GenreScheme(Schema):
    id = fields.Integer()
    name = fields.String()
    title = fields.String()


@ns_movie.route("/")
class MovieViews(Resource):

    def get(self):
        print(request.args.get)
        print(request.args.to_dict())
        movie_query = Movie.query.all()
        # movie_query = Movie.query.paginate(page=1, per_page=4, error_out=True)
        movie_scheme = MovieScheme(many=True)
        # return jsonify(movie_scheme.dump(movie_query.items))

        if request.args.get('director_id'):
            director_id = request.args.get('director_id')
            query = db.session.query(Movie.title, Movie.description, Movie.trailer, Movie.year, Movie.rating,
                                     (Director.name).label('director_name')). \
                join(Director, Movie.director_id == Director.id). \
                where(Director.id == director_id)
            return jsonify(movie_scheme.dump(query))
        if request.args.get('genre_id'):
            query = db.session.query(Movie.title, Movie.description, Movie.trailer, Movie.year,
                                     Movie.rating, (Genre.name).label('name_ganres')).join(Movie,
                                     Movie.genre_id == Genre.id).where(Genre.id == request.args.get('genre_id'))
            return jsonify(movie_scheme.dump(query))
        return jsonify(movie_scheme.dump(movie_query))

    def post(self):
        reg_json = request.json
        add_base = Movie(**reg_json)
        db.session.add(add_base)
        db.session.commit()
        return 200


@ns_movie.route("/<int:uid>")
class MovieView(Resource):
    def get(self, uid):
        movie_query = Movie.query.get(uid)
        movie_scheme = MovieScheme()
        return jsonify(movie_scheme.dump(movie_query))

    def patch(self, uid):
        data = request.json
        query = Movie.query.get(uid)
        if 'id' in data:
            query.id = data['id']
        if 'title' in data:
            query.title = data['title']
        if 'description' in data:
            query.description = data['description']
        if 'trailer' in data:
            query.trailer = data['trailer']
        if 'year' in data:
            query.year = data['year']
        if 'rating' in data:
            query.rating = data['rating']
        if 'genre_id' in data:
            query.genre_id = data['genre_id']
        if 'director_id' in data:
            query.director_id = data['director_id']
        db.session.add(query)
        db.session.commit()
        return 204

    def delete(self, uid):
        query = Movie.query.get(uid)
        db.session.delete(query)
        db.session.commit()
        return 204


@ns_director.route("/")
class DirectorsView(Resource):
    def get(self):
        query = Director.query.all()
        directors_scheme = DirectorScheme(many=True)
        return jsonify(directors_scheme.dump(query))


@ns_director.route("/<int:id_director>")
class DirectorView(Resource):
    def get(self, id_director):
        query = Director.query.get(id_director)
        director_sheme = DirectorScheme()
        return jsonify(director_sheme.dump(query))


@ns_genre.route('/')
class Genres(Resource):
    def get(self):
        query = Genre.query.all()
        genres_scheme = GenreScheme(many=True)
        return jsonify(genres_scheme.dump(query))


@ns_genre.route('/<int:id_genre>')
class Test(Resource):
    def get(self, id_genre):
        querys = db.session.query(Genre.name, Movie.title, Movie.description, Movie.trailer, Movie.year,
                                  Movie.rating).join(Movie, Movie.genre_id == Genre.id).where(
            Genre.id == id_genre)
        genres_scheme = GenreScheme(many=True)
        return jsonify(genres_scheme.dump(querys))


if __name__ == '__main__':
    app.run(debug=True)

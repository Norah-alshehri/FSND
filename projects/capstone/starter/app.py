# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#


@app.route('/')
def homepage():
    return "Welcome"


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def view_movies(payload):
    movies = Movies.query.all()
    if len(movies) == 0:
        abort(404)

    return jsonify({'success': True, 'movies': [movies.format()
                    for movies in movies]}), 200


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movies(payload):
    try:
        request_body = request.get_json()
        if request_body is None:
            abort(422)
        new_movie = Movies(
            request_body['title'],
            request_body['release_date']
            )
        new_movie.insert()
        return jsonify({'success': True}), 200

    except Exception:
        print(sys.exc_info())
        abort(500)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movies(payload, movie_id):
    body = request.get_json()
    movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
    print(movie)
    if movie is None:
        abort(404)

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if new_title is not None:
        movie.title = new_title
    else:
        movie.title = movie.title

    if new_release_date is not None:
        movie.release_date = new_release_date
    else:
        movie.release_date = movie.release_date

    try:
        movie.update()
    except Exception:
        abort(422)
    return jsonify({
            "success": True,
            "Movie": movie.format()
        }), 200


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, movie_id):
    try:
        movie = Movies.query.filter(
                                Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id}), 200

    except Exception:
        print(sys.exc_info())
        abort(422)


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def view_actors(payload):
    actors = Actors.query.all()
    if len(actors) == 0:
        abort(404)
    return jsonify({'success': True, 'actors': [actor.format()
                    for actor in actors]}), 200


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actors(payload):
    try:
        request_body = request.get_json()
        if request_body is None:
            abort(422)
        new_actor = Actors(
            request_body['name'],
            request_body['age'],
            request_body['gender']
            )
        new_actor.insert()
        return jsonify({'success': True}), 200

    except Exception:
        print(sys.exc_info())
        abort(500)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actors(payload, actor_id):
    body = request.get_json()
    actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
    print(actor)
    if actor is None:
        abort(404)

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if new_name is not None:
        actor.name = new_name
    else:
        actor.name = actor.name

    if new_age is not None:
        actor.age = new_age
    else:
        actor.age = actor.age

    if new_gender is not None:
        actor.gender = new_gender
    else:
        actor.gender = actor.gender

    try:
        actor.update()
    except Exception:
        abort(422)
    return jsonify({
            "success": True,
            "Actor": actor.format()
        }), 200


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, actor_id):
    try:
        actor = Actors.query.filter(
                                Actors.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id}), 200

    except Exception:
        print(sys.exc_info())
        abort(422)


# ----------------------------------------------------------------------------#
# error handlers
# ----------------------------------------------------------------------------#

# error handler for 422 implementation
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# error handler for 404 implementation
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


# error handler for 400 implementation
@app.errorhandler(400)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


# error handler for 401 implementation
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'unauthorized'
    }), 401


# error handler for 500 implementation
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


# error handler for AuthError implementation
@app.errorhandler(AuthError)
def auth_errors(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

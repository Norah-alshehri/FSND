import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@[DONE] uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@[DONE] implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = [drinks.short() for drinks in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': drinks
        })


'''
@[DONE] implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = [drinks.long() for drinks in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': drinks
        })


'''
@[DONE] implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
    drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    body = request.get_json()
    if not ('title' in body and 'recipe' in body):
        abort(403)
    drink = Drink(
            title=body.get('title', None),
            recipe=json.dumps(body.get('recipe', None))
        )
    try:
        drink.insert()
    except Exception:
        abort(422)
    return jsonify({
            'success': True,
            'drink': drink.long()
        })


'''
@[DONE] implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
    drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    print(drink)
    if drink is None:
        abort(404)

    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    if new_title is not None:
        drink.title = new_title
    else:
        drink.title = drink.title

    if new_recipe is not None:
        drink.recipe = new_recipe
    else:
        drink.recipe = drink.recipe

    try:
        drink.update()
    except Exception:
        abort(422)
    return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })


'''
@[DONE] implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id
    is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
#require the 'delete:drinks' permission
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    #respond with a 404 error if <id> is not found
    if drink is None:
        abort(404)
    try:
        #delete the corresponding row for <id>
        drink.delete()
        #returns status code 200 and json {"success": True, "delete": id} where id
        #is the id of the deleted record
        return jsonify({
            "success": True,
            "delete": id
        })

    except Exception:
        abort(422)


# Error Handling


'''
@[DONE] implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@[DONE] implement error handler for 404
    error handler should conform to general task above
'''

#error handler for 422 implementation
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

#error handler for 404 implementation
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


#error handler for 400 implementation
@app.errorhandler(400)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


#error handler for 401 implementation
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'unauthorized'
    }), 401


#error handler for 500 implementation
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


'''
@[DONE] implement error handler for AuthError
    error handler should conform to general task above
'''

#error handler for AuthError implementation
@app.errorhandler(AuthError)
def auth_errors(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

import os
import sys
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


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

    '''
    @[DONE]:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    def get_category_list():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return categories

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        categories = get_category_list()
        return jsonify({'success': True,
                        'categories': categories,
                        'total_categories': len(categories)})

    '''
    @[DONE]:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages.
    Clicking on the page numbers should update the questions.
    '''
    def paginate_questions(request, questions_list):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in questions_list]
        paginated_questions = questions[start:end]
        return paginated_questions

    @app.route('/questions',  methods=['GET'])
    def get_questions():
        questions_list = Question.query.all()
        selection = paginate_questions(request, questions_list)
        all_questions = len(selection)
        if all_questions == 0:
            abort(404)

        return jsonify({'success': True,
                        'questions': selection,
                        'total_questions': all_questions,
                        'categories': get_category_list()})

    '''
    @[DONE]:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>',  methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                                    Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id})

        except Exception:
            print(sys.exc_info())
            abort(422)

    '''
    @[DONE]:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''
    @app.route('/questions',  methods=['POST'])
    @cross_origin()
    def create_question():
        try:
            request_body = request.get_json()
            if request_body is None:
                abort(422)
            new_question = Question(
                request_body['question'],
                request_body['answer'],
                request_body['category'],
                request_body['difficulty']
                )
            new_question.insert()
            return jsonify({'success': True})

        except Exception:
            print(sys.exc_info())
            abort(500)

    '''
    @[DONE]:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category>/questions',  methods=['GET'])
    def get_question(category):
        question = []
        question_category = Question.query.filter_by(id=category)
        formatted_question = [question.format() for question in
                              question_category]

        if (len(formatted_question) == 0):
            abort(404)

        return jsonify({'questions': formatted_question,
                        'total_questions': len(formatted_question),
                        'current_category': category})

    '''
    @[DONE]:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search',  methods=['POST'])
    @cross_origin()
    def search_question():
        try:
            search_term = request.get_json().get('searchTerm')
            if search_term:
                result = Question.query.order_by(Question.id).filter(
                        Question.question.ilike(f'%{search_term}%')).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in result],
                'total_questions': len(result),
                'current_category': None
                })
        except Exception:
            print(sys.exc_info())
            abort(404)

    '''
    @[DONE]:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def random_quiz():
        body = request.get_json()
        if body is None:
            abort(422)
        try:
            quiz_category = body.get('quiz_category')
            if quiz_category is None:
                abort(404)
            previous_questions = body.get('previous_questions')
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                            category=quiz_category['id']).all()

            total_questions = [question.format() for question in questions]
            random_question = random.choice(total_questions)

            if random_question['id'] in previous_questions:
                random_question = random.choice(total_questions)

            if len(previous_questions) == len(questions):
                random_question = None

            return jsonify({
              'success': True,
              'question': random_question
            })

        except Exception:
            print(sys.exc_info())
            abort(422)

    @cross_origin()
    def get_quiz():
        request_body = request.get_json()
        if request_body is None:
            abort(400)
        previous_questions = request_body.get('previousQuestions')
        quiz_category = request_body.get('quizCategory')
        question_category = Question.query.filter_by(
                            category=quiz_category).all()
        questions_id = []
        if previous_questions is not None:
            for q in previous_questions:
                questions_id.append(q.get(id))
        print(len(question_category))

        while True:
            question = random.choice(question_category)
            question_category.remove(question)
            if questions_id is not None:
                if question.id not in questions_id:
                    print('true')
                    break

            if (len(question_category) == 0):
                abort(404)
        final_question = [question.format()]
        return jsonify({'showAnswer': False,
                        'currentQuestion': final_question,
                        'previousQuestions': previous_questions})
    '''
    @[DONE]:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400,
                        'message': 'Bad Request'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404,
                        'message': 'Resource Not Found'})

    @app.errorhandler(422)
    def unprossable_entity(error):
        return jsonify({'success': False, 'error': 422,
                        'message': 'Not Processable'})

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 500,
                        'message': 'internal server error'})
    return app

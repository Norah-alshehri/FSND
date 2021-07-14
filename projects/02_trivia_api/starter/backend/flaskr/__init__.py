import os
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
  
  '''
  @[DONE]: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @[DONE]: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
  '''
  @[DONE]: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
     page =  request.args.get('page', 1, type=int)
     start = (page - 1 ) * QUESTIONS_PER_PAGE
     end = start + QUESTIONS_PER_PAGE
     categories=Category.query.all()
     #categories=Category.with_entities(Category.type).all()
     formatted_categories = [ category.format() for category in categories ]
     selection = formatted_categories[start:end]

     if (len(selection) == 0):
        abort(404)

     return  jsonify({'categories':selection})

  '''
    @[DONE]: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
     page =  request.args.get('page', 1, type=int)
     start = (page - 1 ) * QUESTIONS_PER_PAGE
     end = start + QUESTIONS_PER_PAGE
     questions=Question.query.all()
     formatted_questions = [ question.format() for question in questions ]
     selection = formatted_questions[start:end]


     if len(selection) == 0:
        abort(404)


     categories_id = []
     for c in questions:
            categories_id.append(c.category)

     return  jsonify({'questions':selection, 'totalQuestions':len(formatted_questions), 'categories': categories_id, 'currentCategory':5 })


  '''
  @[DONE]: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:ques_id>',  methods=['DELETE'])
  def delete_question(ques_id):

      question = Question.query.filter(Question.id == ques_id).one_or_none()

      if question is None:
         abort(404)

      question.delete()
      questions = Question.query.order_by(Question.id).all()
      formatted_questions = [ question.format() for question in questions]

      if len(formatted_questions) == 0 :
          abort(404)

      return  jsonify({'success':True, 'questions':formatted_questions, 'totalQuestions':len(formatted_questions)})

  '''
  @[DONE]: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',  methods=['POST'])
  @cross_origin()
  def create_question():
      body = request.get_json(force=True)

      if  body==None :
         abort(422)


      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      try:
         question = Question (question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category )
         question.insert()

         selection = Question.query.order_by(Question.id).all()
         page =  request.args.get('page', 1, type=int)
         start = (page - 1 ) * QUESTIONS_PER_PAGE
         end = start + QUESTIONS_PER_PAGE
         current_question = selection[start:end]
         formatted_questions = [ question.format() for question in current_question ]
         
         return  jsonify({'success':True, 'questions':formatted_questions,'totalQuestions':len(formatted_questions)})    
      except:
         abort(422)

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
         question_category=Question.query.filter_by(id=category)
         formatted_question = [ question.format() for question in question_category]

         if (len(formatted_question) == 0):
            abort(404)

         return  jsonify({'questions':formatted_question,'total_questions': len(formatted_question), 'current_category':category })


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
      body = request.get_json()

      search_keyword = body.get('searchTerm', None)


      serch_result = Question.query.filter(Question.question.ilike('%'+search_keyword+'%'))
      formatted_serch_result = [ question.format() for question in serch_result]

      if len(formatted_serch_result) == 0 :
          abort(404)

      return  jsonify({'total_questions':len(formatted_serch_result), 'questions':formatted_serch_result, 'current_category':formatted_serch_result })


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
  @app.route('/quizzes',  methods=['POST'])
  @cross_origin()
  def get_quiz():
         body = request.get_json()

         previous_questions = body.get('previousQuestions', None)
         quiz_category = body.get('quizCategory', None)

         question_category=Question.query.filter_by(category=quiz_category).all()
         
         questions_id = []
         if  previous_questions!=None :
            for q in previous_questions:
               questions_id.append(q.get(id))

         print ( len(question_category))

         while True:
            question = random.choice(question_category)
            question_category.remove(question)
            
            if questions_id!=None :
               if  not question.id in questions_id:
                  print('true')
                  break

            if (len(question_category) == 0):
                abort(404)

         formatted_question = [ question.format() ]
         return  jsonify({'showAnswer': False, 'currentQuestion':formatted_question,'previousQuestions':previous_questions })


  '''
  @[DONE]: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
     return   jsonify({'success':False, 'error':400,'message':'bad request'})


  @app.errorhandler(404)
  def not_found(error):
     return   jsonify({'success':False, 'error':404,'message':'resource not found'})


  @app.errorhandler(422)
  def unprossable_entity(error):
     return   jsonify({'success':False, 'error':422,'message':'unprossable entity'})

   
  @app.errorhandler(500)
  def internal_error(error):
     return   jsonify({'success':False, 'error':500,'message':'internal server error'})


  return app

    
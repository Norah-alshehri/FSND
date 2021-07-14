# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

Ths section present the documentation of endpoints.  

### Endpoints
```
GET '/categories'
GET '/questions'
DELETE '/questions/<int:ques_id>'
POST '/questions'
POST '/questions/search'
POST '/quizzes'
```

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'
- Fetches a list of questions in which the categories are the ids of questions categories.
- Request Arguments: None
- Returns: categories and questions objects with totalQuestions which the the count of questions in DB. 
```
{
  "categories": [
    3,
    4,
    1,
    2,
    6,
    5
  ],
  "currentCategory": 4,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "totalQuestions": 31
}
```

### DELETE '/questions/<int:ques_id>'
- Delete a question based on the provided id.
- Request Arguments: ques_id, witch is the question id
- Returns: Success status of the request and list of all questions along whith thier count.
```
{'success':True, '
questions':formatted_questions,
'totalQuestions':len(formatted_questions)}
```

### POST '/questions'
- Create a new question.
- Request Body: 
```
{"question":"In whtich continent KSA is located?",
   "answer":"Asia",
   "category":3,
   "difficulty":1 }
  ```

- Returns: Success status of the request and list of all questions along whith thier count.
```
{'success':True, '
questions':formatted_questions,
'totalQuestions':len(formatted_questions)}
```

### POST '/categories/<int:category>/questions'
- Fetch questions based on category.
- Request Arguments: category, requested category.
- Returns: List of questions, count of all questions in that category and the current requested category.
```
{'questions':formatted_question,
'total_questions': len(formatted_question),
 'current_category':category }
```

### POST '/questions/search'
- Fetch all questions that contain search term.
- Request Body: search term.
```
{
    "searchTerm":"Asia"
}
```
- Returns: List of all questions, count of all questions in that contain search term and current category.
```
{'total_questions':len(formatted_serch_result), 
'questions':formatted_serch_result, 
'current_category':formatted_serch_result }
```


POST '/quizzes'
- Fetch random question.
- Request Body: List of asked previous questions and the quiz category.
```
{
        "previousQuestions":[
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
        "quizCategory":5
      }
- Returns: Questions, list of asked previous questions and show answer flag to hide the answer from user.
{
  "currentQuestion": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "previousQuestions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "showAnswer": false
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

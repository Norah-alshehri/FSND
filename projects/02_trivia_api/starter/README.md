# Full Stack API Final Project
## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


# Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: internal server error

## Pakages Installation
### Installing Dependencies 
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

5. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

6. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```

## Endpoints
Ths section present the documentation of endpoints.  

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


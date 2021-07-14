import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'postgres:xxxxxx', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    [DONE]
    Write at least one test for each test for successful operation
    and for expected errors.
    """
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['question'])
        self.assertTrue(data['totat_question'])
        self.assertTrue(len(data['question']))

    def test_delete_question(self):
        res = self.client().delete('/questions/7000')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 404)
        self.assertEqual(res.data['current_category'], "resource not found")
        self.assertEqual(data['current_category'], False)

    def test_post_question(self):
        res = self.client().post('/questions',  json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])

    def test_post_search_question(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['question']))

    def test_get_category_question(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['question']))

    def test_post_play_quiz(self):
        res = self.client().post('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['question']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

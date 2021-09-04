import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'norah')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
        self.DB_NAME = os.getenv('DB_NAME', 'capstone')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
                                            self.DB_USER, self.DB_PASSWORD,
                                            self.DB_HOST, self.DB_NAME)

        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# ----------------------------------------------------------------------------#
# Authorization token to start testing 
# ----------------------------------------------------------------------------#

        self.casting_assistant = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
        }
        self.casting_director = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
        }
        self.executive_producer = {
            "Authorization": "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))
        }

# ----------------------------------------------------------------------------#
# Tests for success behavior of each endpoint
# ----------------------------------------------------------------------------#
# Movies endpoint
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])

    def test_post_movies(self):
        res = self.client().post('/movies', headers=self.executive_producer, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_movies(self):
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['movies'],1)

    def test_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

# Actors endpoint
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])

    def test_post_actors(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/1')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['actors'], 1)
        
    def test_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)
# ----------------------------------------------------------------------------#
# Tests for error behavior of each endpoint
# ----------------------------------------------------------------------------#
# Movies endpoint
    def test_get_movies_failed(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_post_movies_failed(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_movies_failed(self):
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movies_failed(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Actors endpoint
    def test_get_actors_failed(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_post_actors_failed(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_actors_failed(self):
        res = self.client().patch('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actors_failed(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# ----------------------------------------------------------------------------#
# Tests of RBAC for each role
# ----------------------------------------------------------------------------#
# Casting Assistant
1
2
# Executive Producer
1
2
# Casting Director
1
2

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()



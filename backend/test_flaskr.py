from dataclasses import dataclass
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
        # self.database_path = "postgres://{}:{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'Passw0rd1', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_trivia_questions = {
            'question': 'Who is the Gang leader of the Peaky Blinders',
            'answer': 'Tommy Shelby',
            'difficulty': '3',
            'category': '5'
        }
        
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_pagination(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        
    def test_404_invalid_pageNo(self):
        response = self.client().get('/questions?page=50')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
        
    def test_delete_Question(self):
        response = self.client().delete('/questions/6')
        data = json.loads(response.data)
        
        question = Question.query.filter(Question.id == 6).one_or_none()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
    
    def test_404_if_doesnt_exist(self):
        response = self.client().delete('/questions/50')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_create_new_trivia_questions(self):
        response = self.client().post('/questions', json = self.new_trivia_questions)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    
    def test_404_if_trivia_creation_not_allowed(self):
        response = self.client().post('/questions/50', json = self.new_trivia_questions)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    
    def test_search_Question(self):
        response = self.client().post('/questions')
        data = json.loads(response.data)
        
        # question = Question.query.filter(Question.question == 'Dutch')
        search_result = Question.query.filter(Question.question.ilike('%Dutch%'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['Search_Result'], 'Dutch')
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(search_result, None)
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
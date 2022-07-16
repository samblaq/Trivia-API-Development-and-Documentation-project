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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'Passw0rd1', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_trivia_questions = {
            'question': 'Who is the Gang leader of the Peaky Blinders',
            'answer': 'Tommy Shelby',
            'difficulty': '3',
            'category': '5'
        }
        
        self.new_trivia_questions_failed = {
            'question': 'Who is the Gang leader of the Peaky Blinders',
            'answer': 'Tommy Shelby',
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
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_invalid_pageNo(self):
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_delete_Question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)
        question = Question.query.filter(Question.id == 1).one_or_none()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)
    
    def test_404_if_doesnt_exist(self):
        response = self.client().delete('/questions/100')
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
        response = self.client().post('/questions', json = self.new_trivia_questions_failed)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_Question(self):
        response = self.client().post('/questions',json = {"search": "value"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_search_Question_failed(self):
        response = self.client().post('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertTrue(data['message'], 'Bad Request')
    

    def test_question_category(self):
        response = self.client().get('/categories/5/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
    
    def test_question_category_invalid(self):
        response = self.client().get('/categories/7/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')

    def test_quiz(self):
        response = self.client().post('/quizzes', json = {'previous_questions':[],'quiz_category':{'type': 'Science', 'id':'2'}})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
    def test_quiz_failed(self):
        response = self.client().post('/quizzes')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertTrue(data['message'], 'Bad request')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
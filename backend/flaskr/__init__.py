import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION")
        return response
    
    # This is a pagination function
    def pagination_trivia(request,selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        
        return current_questions
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")   
    def get_category():
        try:
            categories = Category.query.all()
            
            if categories is None:
                abort(404)
            formatted_category = {category.id: category.type for category in categories}
            
            return jsonify({
                "success": True,
                "categories": formatted_category
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            selection = Question.query.all()
            
            categories = Category.query.all()
            formatted_category = {category.id: category.type for category in categories}
            if selection is None:
                abort(404)
                
            questions = pagination_trivia(request,selection)
            return jsonify(
                {
                    "success": True,
                    "categories": formatted_category,
                    "questions": questions,
                    "total_questions": len(selection),
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
                abort(404)
                
            question.delete()
            
            selection = Question.query.all()
            questions = pagination_trivia(request,selection)
            return jsonify({
                "success": True,
                "deleted":question_id,
                # "questions": question,
                "total_questions": len(selection),
            })
        except:
            abort(422)
        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json(Question)
        add_new_question = body.get("question",None)
        add_new_answer = body.get("answer",None)
        add_new_difficulty = body.get("difficulty",None)
        add_new_category = body.get("category",None)
        
        question = Question(question = add_new_question, answer = add_new_answer, category = add_new_category, difficulty = add_new_difficulty)
        question.insert()
        selection = Question.query.all()
        
        questions = pagination_trivia(request,selection)
        return jsonify({
            "success": True,
            "created": question.id,
            "questions": questions,
        })


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route("/questions/search", methods=["POST"])
    def get_search():
        search_term = request.args.get('search', None)
        if search_term is not None:
            search_result = Question.query.filter(Question.question.ilike('%'+search_term+'%'))
            formatted_search= [result.format() for result in search_result]
            return jsonify({
                "success": True,
                "questions": formatted_search,
                "searches": len(formatted_search),
                "search_result": search_term
            })
        else:
            abort(422)

    """
    @TODO:
    

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_category(category_id):
        category = Category.query.get(category_id)
        try:
            
            if category_id is None:
                abort(404)
                
            by_category = Question.query.filter(Question.category == category_id).all()
            
            questions = pagination_trivia(request,by_category)
                
            return jsonify({
                "success": True,
                "category_id": category.id,
                "questions": questions,
                "total_questions": len(questions),
            })
        except:
            abort(422)
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def category_question():
        body = request.get_json(Question)
        prev_questions = body.get('previous_questions',None)

        quiz_category = body.get('quiz_category')['id']

        if (prev_questions is None):
            abort(400)

        questions = []
        if quiz_category == 0:
            questions = Question.query.filter(Question.id.notin_(prev_questions)).all()
        else:
            category = Category.query.get(quiz_category)
            if category is None:
                abort(404)
            questions = Question.query.filter(Question.id.notin_(prev_questions), Question.category == quiz_category).all()
        main_question = None
        if (len(questions) > 0):
            index = random.randrange(0, len(questions))
            main_question = questions[index].format()
        return jsonify({
            'success': True,
            'question': main_question,
            'total_questions': len(questions)
        })
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"
        }), 400
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server Error"
        }), 500
        
    return app

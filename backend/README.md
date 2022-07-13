# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers. - Done
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. - Done
3. Create an endpoint to handle `GET` requests for all available categories. - Done
4. Create an endpoint to `DELETE` a question using a question `ID`. - Done
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. - Done
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

`GET '/questions'`

- Fetch a list of 10 questions which include a pagination
- Request Arguments: None
- Returns: Returns a questions object containing (question, answer, difficulty,category)
```json
{
  "categories":
    { "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
    },
  "questions":[
    { "answer":"Muhammad Ali",
      "category":4,
      "difficulty":1,
      "id":9,
      "question":"What boxer's original name is Cassius Clay?"
    }],"success":true,"total_questions":18
}
```

`DELETE '/questions/<int:question_id>'`
- deletes a specific question with reference to the question ID
- Request Arguments: question_id
- Returns: Returns the deleted question ID and the len of the remaining questions based on the question ID

```json
{
  "deleted":25,
  "success":true,
  "total_questions":14
}
```

`POST '/questions'`
- This endpoint post new questions (questions, answer, difficulty,category) into the database
- Request Arguments: Request values for (questions, answer, difficulty,category) from the body
- Returns: Returns the newly created question ID, the success message and all the questions in the database

```json
{
  "created":27,
    "questions":[
      {
        "answer":"Brazil",
        "category":6,
        "difficulty":3,
        "id":10,
        "question":"Which is the only team to play in every soccer World Cup tournament?"
      }
    ],
  "success":true
}
```

`POST '/questions/search'`
- Fetches the questions based on the search parameters/term.
- Request Arguments: Searh Term
- Returns the value of the search parameter, number of searches, success message and the question details based on the search parameters.

```json
{
  "questions":[
    { "answer":"Lake Victoria",
      "category":3,
      "difficulty":2,
      "id":13,
      "question":"What is the largest lake in Africa?"
    }],
  "search_result":"Africa",
  "searches":1,
  "success":true
}
```

`GET '/categories/<int:category_id>/questions' `
- Fetches every question uder the category supplied in the endpoint
- Returns Arguments: category_id
- Returns the Catgory ID and the all the questions associated with the category and also the success message and count of the number of questions

```json
{
  "category_id":1,
    "questions":[{
      "answer":"The Liver",
      "category":1,
      "difficulty":4,
      "id":20,
      "question":"What is the heaviest organ in the human body?"
      },
      {
      "answer":"Alexander Fleming",
      "category":1,
      "difficulty":3,
      "id":21,
      "question":"Who discovered penicillin?"}
      ],
    "success":true,
    "total_questions":2
  }
```

`POST '/quizzes' `
- This endpoint feteches random questions based on the category id and the previous questions parameter to play the quiz.
- Request Arguments: Category and previous question parameters
- Returns random questions within the given category and the previous question parameters

```json
{
  "question":{
    "answer":"Escher",
    "category":2,
    "difficulty":1,
    "id":16,
    "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
  "success":true
}
```
### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

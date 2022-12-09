# Developer Life Support API

![Django CI](https://github.com/insper-education/active-handout-plugins-py/actions/workflows/django.yml/badge.svg)

## Running locally

### Setup

Create and activate a virtual environment, then install the dependencies:

```
$ cd backend
$ python -m venv env --prompt .
$ . env/bin/activate
$ pip install -r requirements.txt
```

Finally, generate the database and apply migrations:

```
$ python manage.py migrate
```

### Running the server

```
$ python manage.py runserver
```

## Running with Docker

    docker build -t active_handout_api .

    # To run locally
    docker run -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=db postgres:13.0-alpine

    # For testing run both commands simultaneously (on different terminals)
    docker run -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=test_db postgres:13.0-alpine
    docker run -v $PWD:/app -p 8000:8000 active_handout_api

## API Documentation

Once you are running the server you can check the API documentation in the home page.

# Overview

This Flask application contains a simple web application that allows users to buy a number of Products in the store.

An HTML form is used to allow users to enter the number of Products they wish to buy.

# Database

The database is a SQLite database that is stored in the `app/database.db` file. The database contains the following tables (for details on the schema, see `schema.sql` or the `app/models.py` module):

![Image](/schema.png "Schema")

# Testing

Pytest is used to test the application. To run all the tests:

```sh
(venv) $ python -m pytest -v
```

Code coverage of the tests:

```sh
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/__init__.py      13      0   100%
app/config.py        26      0   100%
app/main.py           7      7     0%   1-10
app/models.py        50      4    92%   21, 43, 60, 74
app/store.py         82     23    72%   40-42, 46, 82-84, 98, 101-103, 129-141, 158-159
-----------------------------------------------
TOTAL               178     34    81%
```


# Running the application

To run the application with Docker, you need to create a ```.env``` file with the following content:

```sh
SECRET_KEY=your-secret-key
SESSION_COOKIE_NAME=session_name
PROD_DATABASE_URI=sqlite:///database.db
DEV_DATABASE_URI=sqlite:///database.db
```

Create and run the container using docker-compose:

```sh
$ docker-compose up
```

Then the application will be accessible at http://localhost.
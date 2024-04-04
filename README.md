Flaskr - SQLAlchemy
===================

The basic blog app built in the Flask [tutorial](https://flask.palletsprojects.com/tutorial/)...

...with extra extensions :
- SQLAlchemy
- Flask-Migrate
- Flask-Login


Install
-------

Create a virtualenv and activate it::

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install dependancies::

    $ pip install -r requirements.txt

Init Database
-------------

    $ flask db init
    $ flask db upgrade

Run
---

    $ flask --debug run 

Open http://127.0.0.1:5000 in a browser.


Test
----

    $ pytest tests/

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

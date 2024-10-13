# Overview
This Flask application offers a way to search the content of  magazines digitized by *Biblioteca Centrală Universitară "Lucian Blaga" Cluj-Napoca*(*"Lucian Blaga" Central University Library of Cluj-Napoca*) at [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html).
The app was created mostly for learning purposes but it also tries to add a functionality that is missing from the library website.

# Demo App Installation Instructions
A demo version of this app can be run locally by following the next steps. 

Pull down the source code from GitHub:\
`https://github.com/AndreiIav/Darwin_App`

Create a new virtual environment

Activate the virtual environment

Install the python packages specified in requirements.txt:\
`(venv) $ pip install -r requirements.txt`

In order for the app to run, a SQLite database with correct data is needed.\
The demo database can be created using this command:
`(venv) $ flask database create demo`

The demo SQLite database can be deleted using this command:
`(venv) $ flask database remove demo`

# Running the demo version of the application
Run the development server to serve the demo Flask application:
`(venv) $ flask --app wsgi_demo run`

Navigate to 'http://127.0.0.1:5000/' in your favorite web browser to view the website !
Note: the demo database offers access to two magazines and their data. Some keywords that will yield results are: 'transilvania', 'bucuresti', 'scoala'.

# Key Python Modules Used
- **Flask**: a micro-framework for web application development
- **Flask-SQLAlchemy**:  ORM (Object Relational Mapper) for Flask
- **Flask-WTF**: a Flask extension that integrates the WTForms library, which provides useful features for creating and handling forms in a simple way for a Flask web application
- **Flask-Caching**: a Flask extension that adds caching support for various backends
- **pytest**: framework for testing Python projects
- **pytest-cov**: pytest extension for running coverage\.py to check code coverage of tests
- **pytest-playwright**:  a Pytest plugin to write end-to-end tests
- **python-dotenv**: a Python library for reading .env files

This application is written using Python 3.11.

# Key Features
- **ability to search after keywords**
- **filter results by magazine name**
- **see previews of results with the keyword highlighted**
- **display the details of the magazine where a result was found**
- **ability to access the magazine on the library website by following its link**

# Technical Features
### Logging
- In **development**, **test** and **demo** the app utilizes `concurrent_log_handler` for concurrent access to log files.
- In **production**, logging is handled by Gunicorn, which is configured to manage and log server activity efficiently.

### Caching
- In **development**, **test** and **demo**, caching is implemented using `Flask-Caching` with the `SimpleCache` backend for quick, in-memory caching.
- In **production**, `Flask-Caching` is configured with a Redis backend to provide more robust, persistent caching.

### Deployment
- In **production**, the app is served using **Nginx** as a reverse proxy and **Gunicorn** as the WSGI application server. 

# Testing
In order for the tests to run, a SQLite test database with correct data is needed.\
A test database can be creating using this command:
`(venv) $ flask database create test`

To run all the tests:\
`(venv) $ pytest`

To check the code coverage of the tests:\
`(venv) $ pytest --cov-report term-missing --cov=application`

The test SQLite database can be deleted using this command:
`(venv) $ flask database remove test`

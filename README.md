# Overview
This Flask application offers a way to search the content of  magazines digitized by *Biblioteca Centrală Universitară "Lucian Blaga" Cluj-Napoca*(*"Lucian Blaga" Central University Library of Cluj-Napoca*) at [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html).
The app was created mostly for learning purposes but it also tries to add a functionality that is missing from the library website.

# Website link
This app can be accessed at: [https://heritage-lib.com](https://heritage-lib.com).

# Key Features
- **ability to search after keywords**
- **filter results by magazine name**
- **see previews of results with the keyword highlighted**
- **display the details of the magazine where a result was found**
- **ability to access the magazine on the library website by following its link**

# Technical Features
### Querying Data
- The app leverages the _SQLite_ _FTS5_ extension to enable efficient and fast full-text search capabilities.

### Rendering Dynamic and Responsive Pages
- The app utilizes _Jinja2_ templating engine to dynamically render HTML pages.
- The app incorporates _Bootstrap_ to create responsive pages.

### Logging
- In **development**, **test** and **demo** the app utilizes _concurrent_log_handler_ for concurrent access to log files.
- In **production**, logging is handled by _Gunicorn_, which is configured to manage and log server activity efficiently.

### Caching
- In **development**, **test** and **demo**, caching is implemented using _Flask-Caching_ with the _SimpleCache_ backend for quick, in-memory caching.
- In **production**, _Flask-Caching_ is configured with a _Redis_ backend to provide more robust, persistent caching.

### Deployment
- In **production**, the app is served using _Nginx_ as a reverse proxy and _Gunicorn_ as the WSGI application server. 

# Demo App Installation Instructions
A demo version of this app can be run locally by following the next steps. 

Pull down the source code from GitHub:\
`git clone https://github.com/AndreiIav/Darwin_App`

Change the current working directory to the 'Darwin_App' directory. 

Create and activate a virtual environment:\
On Linux:\
Create the virtual environment:\
`python3 -m venv venv`\
Activate the virtual environment:\
`source venv/bin/activate`

On Windows:\
Create the virtual environment:\
`python -m venv venv`\
Activate the virtual environment:\
`venv\Scripts\activate`

**Note**: all the following shell commands need to be run from a virtual environment.

Install the python packages specified in requirements.txt:\
`pip install -r requirements.txt`

In order for the app to run, a SQLite database with correct data is needed.\
The demo database can be created using this command:\
`flask database create demo`

(When needed) the demo SQLite database can be deleted using this command:\
`flask database remove demo`

# Running the demo version of the application
Run the development server to serve the demo Flask application:\
`flask --app wsgi_demo run`

Navigate to 'http://127.0.0.1:5000/' in your favorite web browser to view the website !\
**Note**: the demo database offers access to two magazines and their data.
Some keywords that will yield results are: 'transilvania', 'bucuresti', 'scoala'.

# Testing
In order for the tests to run, a SQLite test database with correct data is needed.\
A test database can be created using this command:\
`flask database create test`

To run all unit and functional tests:\
`pytest -k "not end-to-end"`

To run end-to-end tests, first install Playwright browsers and dependencies:\
`playwright install --with-deps`

Run end-to-end tests:\
`pytest -k end-to-end`

To check the code coverage of the tests:\
`pytest --cov-report term-missing --cov=application`

The test SQLite database can be deleted using this command:\
`flask database remove test`

# Key Python Modules Used
- **Flask**: a micro-framework for web application development
- **Flask-SQLAlchemy**:  ORM (Object Relational Mapper) for Flask
- **Flask-WTF**: a Flask extension that integrates the WTForms library, which provides useful features for creating and handling forms in a simple way for a Flask web application
- **Flask-Caching**: a Flask extension that adds caching support for various backends
- **pytest**: framework for testing Python projects
- **pytest-cov**: pytest extension for running coverage\.py to check code coverage of tests
- **pytest-playwright**:  a Pytest plugin to write end-to-end tests
- **python-dotenv**: a Python library for reading .env files


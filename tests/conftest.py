import os
import sqlite3
import subprocess
import time

import pytest

from application import init_app
from application.search_page.search_page_data_repository import (
    get_details_for_searched_term,
    paginate_results,
    store_s_word_in_session,
)


@pytest.fixture(scope="module")
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    app = init_app()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def test_cli_app():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"

    app = init_app()

    yield app


@pytest.fixture(scope="module")
def start_app_server():
    # Specify the port for the Flask app to run on
    port = os.environ.get("FLASK_RUN_PORT", 5001)  # Default to 5001 if not set

    # Set the Testing configuration prior to starting the app server
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"

    # Start the Flask app in a subprocess with the specified port
    process = subprocess.Popen(["flask", "run", "--port", str(port)])
    # Wait a few seconds for the server to start
    time.sleep(1)

    server_address = f"http://localhost:{port}"

    yield server_address

    # Terminate the Flask app after tests are done
    process.terminate()
    process.wait()


@pytest.fixture
def s_word_in_session():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    app = init_app()

    with app.test_request_context(
        "/results/search", query_string={"search_box": "fotbal"}
    ):
        yield store_s_word_in_session


@pytest.fixture(scope="class")
def set_up_data_for_previews_for_page_id():
    s_word = "andrei mocioni"
    formatted_s_word = "andrei+mocioni"
    details_searched_term = get_details_for_searched_term(formatted_s_word)
    # get only one result by setting per_page = 1
    paginated_details_for_searched_term = paginate_results(
        details_searched_term, page=1, per_page=1, error_out=False
    )
    page_id = list(paginated_details_for_searched_term)[0][-1]

    return (s_word, page_id, paginated_details_for_searched_term)


@pytest.fixture
def create_test_db(tmp_path):
    path_db = tmp_path / "test.db"
    conn = sqlite3.connect(path_db)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executescript(
            """
            CREATE TABLE magazines(
            id integer PRIMARY KEY ,
            name text,
            magazine_link text);

            CREATE TABLE magazine_year(
            id integer PRIMARY KEY,
            magazine_id integer,
            year text,
            magazine_year_link text,
            FOREIGN KEY(magazine_id) REFERENCES magazines(id));

            CREATE TABLE magazine_number(
            id integer PRIMARY KEY,
            magazine_year_id integer,
            magazine_number text,
            magazine_number_link text,
            FOREIGN KEY(magazine_year_id) REFERENCES magazine_year(id));

            CREATE TABLE magazine_number_content(
            id integer PRIMARY KEY,
            magazine_number_id integer,
            magazine_content text,
            magazine_page id,
            FOREIGN KEY(magazine_number_id) REFERENCES magazine_number(id));
            """
        )

    yield path_db


@pytest.fixture
def insert_data_in_magazines_table(create_test_db):
    database_path = create_test_db
    data = [
        (1, "magazine_name_1", "magazine_link_1"),
        (2, "magazine_name_2", "magazine_link_2"),
    ]

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executemany(
            "INSERT INTO magazines(id,name,magazine_link) VALUES(?,?,?)",
            data,
        )

    yield database_path


@pytest.fixture
def insert_data_in_magazine_year_table(insert_data_in_magazines_table):
    database_path = insert_data_in_magazines_table
    data = [
        (1, 1, "year_1", "year_link_1"),
        (2, 1, "year_2", "year_link_2"),
    ]

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executemany(
            "INSERT INTO magazine_year(id,magazine_id,year,magazine_year_link) VALUES (?,?,?,?)",
            data,
        )

    yield database_path


@pytest.fixture
def insert_data_in_magazine_number_table(insert_data_in_magazine_year_table):
    database_path = insert_data_in_magazine_year_table
    data = [
        (1, 1, "number_1", "number_link_1"),
        (2, 1, "number_2", "number_link_2"),
    ]

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executemany(
            "INSERT INTO magazine_number(id,magazine_year_id,magazine_number,magazine_number_link) VALUES (?,?,?,?)",
            data,
        )

    yield database_path


@pytest.fixture
def insert_data_in_magazine_number_content_table(insert_data_in_magazine_number_table):
    database_path = insert_data_in_magazine_number_table
    data = [
        (1, 1, "magazine_content_1", 1),
        (2, 1, "magazine_content_2", 2),
    ]

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executemany(
            "INSERT INTO magazine_number_content(id,magazine_number_id,magazine_content,magazine_page) VALUES(?,?,?,?)",
            data,
        )

    yield database_path

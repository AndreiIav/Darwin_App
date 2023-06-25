import os
import pytest


from application import init_app

from application.home.logic import (
    get_existent_magazines,
    get_magazine_name,
    get_magazine_details,
)

from application.search_page.logic import (
    store_s_word_in_session,
    format_search_word,
    get_distinct_magazine_names_and_count_for_searched_term,
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    paginate_results,
)


@pytest.fixture
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    app = init_app()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


@pytest.fixture
def s_word_in_session():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    app = init_app()

    with app.test_request_context(
        "/search_page.search_page_bp/search", query_string={"search_box": "fotbal"}
    ):
        yield store_s_word_in_session


@pytest.fixture
def existent_magazines():
    existent_magazines = get_existent_magazines()
    return existent_magazines


@pytest.fixture
def magazine_name():
    return get_magazine_name


@pytest.fixture
def magazine_details():
    return get_magazine_details


@pytest.fixture
def format_word():
    return format_search_word


@pytest.fixture
def distinct_magazine_names_and_count_for_searched_term():
    return get_distinct_magazine_names_and_count_for_searched_term


@pytest.fixture
def details_for_searched_term():
    return get_details_for_searched_term


@pytest.fixture
def details_for_searched_term_for_specific_magazine():
    return get_details_for_searched_term_for_specific_magazine


@pytest.fixture
def paginate():
    return paginate_results

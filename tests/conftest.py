import os
import pytest
from application import init_app
from application.search_page.logic import (
    store_s_word_in_session,
    get_details_for_searched_term,
    paginate_results,
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
    s_word = "stefan michailescu"
    formatted_s_word = "stefan+michailescu"
    details_searched_term = get_details_for_searched_term(formatted_s_word)
    paginated_details_for_searched_term = paginate_results(
        details_searched_term, page=1, per_page=1, error_out=False
    )
    page_id = list(paginated_details_for_searched_term)[0][-1]

    return (s_word, page_id, paginated_details_for_searched_term)

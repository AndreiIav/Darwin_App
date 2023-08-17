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
    replace_multiple_extra_white_spaces_with_just_one,
    get_magazine_content_details,
    convert_diacritics_to_basic_latin_characters,
    get_indexes_for_highlighting_s_word,
    get_distinct_s_word_variants,
    add_html_mark_tags_to_the_searched_term,
    get_all_start_and_end_indexes_for_preview_substrings,
    merge_overlapping_preview_substrings,
    get_preview_string,
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


@pytest.fixture
def replace_white_spaces():
    return replace_multiple_extra_white_spaces_with_just_one


@pytest.fixture
def magazine_content_details():
    return get_magazine_content_details


@pytest.fixture
def convert_diacritics_to_basic_characters():
    return convert_diacritics_to_basic_latin_characters


@pytest.fixture
def get_indexes_for_highlighting_word():
    return get_indexes_for_highlighting_s_word


@pytest.fixture
def get_distinct_word_variants():
    return get_distinct_s_word_variants


@pytest.fixture
def add_html_mark_tags_around_term():
    return add_html_mark_tags_to_the_searched_term


@pytest.fixture
def get_start_end_indexes_for_preview():
    return get_all_start_and_end_indexes_for_preview_substrings


@pytest.fixture
def merge_overlapping_substrings():
    return merge_overlapping_preview_substrings


@pytest.fixture
def preview_string():
    return get_preview_string

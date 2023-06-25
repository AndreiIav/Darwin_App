import pytest
import flask_sqlalchemy
from flask import request

# Tests for get_existent_magazines()
def test_content_of_get_existent_magazines(test_client, existent_magazines):
    existent_magazine = ("Viaţa Noastră (1936-1937)", 153)
    non_existent_magazine = ("abc", 0)

    assert existent_magazine in existent_magazines
    assert non_existent_magazine not in existent_magazines


def test_instance_of_get_existent_magazines(test_client, existent_magazines):
    assert isinstance(existent_magazines, flask_sqlalchemy.query.Query)


def test_length_of_get_existent_magazines(test_client, existent_magazines):
    assert len(list(existent_magazines)) == 132


# Tests for get_magazine_name()
def test_get_magazine_name_with_existent_magazine_id(test_client, magazine_name):
    test_magazine = "Buletinul eugenic şi biopolitic (1927-1947)"

    assert test_magazine == magazine_name(33)
    assert test_magazine == magazine_name("33")


def test_get_magazine_name_with_non_existent_magazine_id(test_client, magazine_name):
    assert magazine_name(999) is None
    assert magazine_name("999") is None


def test_get_magazine_name_with_no_parameter_passed(test_client, magazine_name):
    assert magazine_name() is None


invalid_magazine_id_input = ["a", True, 1.23, None]


@pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
def test_get_magazine_name_with_invalid_data_types_parameters(
    test_client, magazine_name, invalid_magazine_id
):
    assert magazine_name(invalid_magazine_id) is None


# Tests for get_magazine_details()
@pytest.mark.parametrize("magazine_id", [13, "13"])
def test_get_magazine_details_with_existent_magazine_id(
    test_client, magazine_details, magazine_id
):
    test_magazine_details = [("ANUL 1 1868", 24, 759), ("ANUL 2 1871", 2, 72)]

    for index, magazine_detail in enumerate(magazine_details(magazine_id)):
        assert test_magazine_details[index] == magazine_detail


def test_get_magazine_details_with_not_existent_magazine_id(
    test_client, magazine_details
):

    assert len(list(magazine_details(999))) == 0


def test_get_magazine_details_with_no_parameter_passed(test_client, magazine_details):
    assert len(list(magazine_details())) == 0


@pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
def test_get_magazine_details_with_invalid_data_types_parameters(
    test_client, magazine_details, invalid_magazine_id
):
    assert len(list(magazine_details(invalid_magazine_id))) == 0


# Tests for store_s_word_in_session()
def test_store_s_word_in_session_when_s_word_not_in_session_and_a_request_s_word_is_provided(
    s_word_in_session,
):
    session_s_word = None
    request_s_word = request.args.get("search_box")
    s_word = s_word_in_session(session_s_word, request_s_word)

    assert s_word == "fotbal"


def test_store_s_word_in_session_when_s_word_not_in_session_and_a_request_s_word_is_not_provided(
    s_word_in_session,
):
    session_s_word = None
    request_s_word = None
    s_word = s_word_in_session(session_s_word, request_s_word)

    assert s_word is None


def test_store_s_word_in_session_with_s_word_alredy_stored_in_session_and_same_request_s_word_provided(
    s_word_in_session,
):
    request_s_word = request.args.get("search_box")
    session_s_word = s_word_in_session(None, request_s_word)
    s_word = s_word_in_session(session_s_word, request_s_word)

    assert s_word == "fotbal"


def test_store_s_word_in_session_with_s_word_alredy_stored_in_session_and_diferent_request_s_word_provided(
    s_word_in_session,
):
    request_s_word = request.args.get("search_box")
    session_s_word = s_word_in_session(None, request_s_word)
    request_s_word = "tennis"
    s_word = s_word_in_session(session_s_word, request_s_word)

    assert s_word == "tennis"


# Tests for format_search_word
def test_format_s_word_with_one_word_as_input(test_client, format_word):

    formatted_s_word = format_word("darwin")
    assert formatted_s_word == "darwin"


def test_format_s_word_with_multiple_words_as_input(test_client, format_word):

    formatted_s_word = format_word("Victor Babeș")
    assert formatted_s_word == "Victor+Babeș"

    formatted_s_word = format_word("ala bala portocala")
    assert formatted_s_word == "ala+bala+portocala"


# Tests for get_distinct_magazine_names_and_count_for_searched_term
def test_instance_of_get_distinct_magazine_names_and_count_for_searched_term(
    test_client, distinct_magazine_names_and_count_for_searched_term
):

    magazine_names_and_count = distinct_magazine_names_and_count_for_searched_term(
        "fotbal"
    )
    assert isinstance(magazine_names_and_count, flask_sqlalchemy.query.Query)


def test_response_details_of_get_distinct_magazine_names_and_count_for_searched_term(
    test_client, distinct_magazine_names_and_count_for_searched_term
):

    magazine_names_and_count = distinct_magazine_names_and_count_for_searched_term(
        "fotbal"
    )

    for row in magazine_names_and_count:
        assert len(row) == 2

    for name, count in magazine_names_and_count:
        assert isinstance(name, str)
        assert isinstance(count, int)


# Tests for get_details_for_searched_term
def test_instance_of_get_details_for_searched_term(
    test_client, format_word, details_for_searched_term
):

    s_word = format_word("Constantin Esarcu")
    details_for_searched_term = details_for_searched_term(s_word)

    assert isinstance(details_for_searched_term, flask_sqlalchemy.query.Query)


def test_response_details_of_get_details_for_searched_term(
    test_client, format_word, details_for_searched_term
):

    s_word = format_word("Constantin Esarcu")
    details_for_searched_term = details_for_searched_term(s_word)

    for row in details_for_searched_term:
        assert len(row) == 6

    for name, year, number, page, link, rowid in details_for_searched_term:
        assert isinstance(name, str)
        assert isinstance(year, str)
        assert isinstance(number, str)
        assert isinstance(page, int)
        assert isinstance(link, str)
        assert isinstance(rowid, int)

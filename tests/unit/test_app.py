import pytest
import flask_sqlalchemy
from flask import request

# Test Data for parametrized tests
invalid_magazine_id_input = ["a", True, 1.23, None]


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

import pytest
import flask_sqlalchemy


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
def test_magazine_name_with_existent_magazine_id(test_client, magazine_name):
    assert magazine_name(33)
    assert magazine_name("33")


def test_magazine_name_with_non_existent_magazine_id(test_client, magazine_name):
    assert magazine_name(999) is None
    assert magazine_name("999") is None


def test_magazine_name_with_no_parameter_passed(test_client, magazine_name):
    assert magazine_name() is None


def test_magazine_name_with_invalid_data_types_parameters(test_client, magazine_name):
    assert magazine_name("a") is None
    assert magazine_name(True) is None
    assert magazine_name([]) is None
    assert magazine_name(1.23) is None
    assert magazine_name(None) is None

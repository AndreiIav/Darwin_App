import pytest
import flask_sqlalchemy

from application.home.logic import (
    get_existent_magazines,
    get_magazine_name,
    get_magazine_details,
)


# Tests for get_existent_magazines()
class TestGetExistentMagazines:
    def test_content_of_get_existent_magazines(self, test_client):
        existent_magazine = ("Albina (1866-1876)", 4)
        non_existent_magazine = ("abc", 0)

        assert existent_magazine in get_existent_magazines()
        assert non_existent_magazine not in get_existent_magazines()

    def test_instance_of_get_existent_magazines(self, test_client):
        assert isinstance(get_existent_magazines(), flask_sqlalchemy.query.Query)

    def test_length_of_get_existent_magazines(self, test_client):
        assert len(list(get_existent_magazines())) == 2


# Tests for get_magazine_name()
class TestGetMagazineName:
    def test_get_magazine_name_with_existent_magazine_id(self, test_client):
        test_magazine = "Albina (1866-1876)"

        assert test_magazine == get_magazine_name(4)

    def test_get_magazine_name_with_non_existent_magazine_id(self, test_client):
        assert get_magazine_name(999) is None
        assert get_magazine_name("999") is None

    def test_get_magazine_name_with_no_parameter_passed(self, test_client):
        assert get_magazine_name() is None

    invalid_magazine_id_input = ["a", True, 1.23, None, "33"]

    @pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
    def test_get_magazine_name_with_invalid_data_types_parameters(
        self, test_client, invalid_magazine_id
    ):
        assert get_magazine_name(invalid_magazine_id) is None

    def test_get_magazine_name_if_OverflowError_returns_None(self, test_client):
        assert get_magazine_name(99999999999999999999) is None


# Tests for get_magazine_details()
class TestGetMagazineDetails:
    @pytest.mark.parametrize("magazine_id", [13, "13"])
    def test_get_magazine_details_with_existent_magazine_id(
        self, test_client, magazine_id
    ):
        test_magazine_details = [("ANUL 1 1868", 24, 757), ("ANUL 2 1871", 2, 72)]

        for index, magazine_detail in enumerate(get_magazine_details(magazine_id)):
            assert test_magazine_details[index] == magazine_detail

    def test_get_magazine_details_with_not_existent_magazine_id(self, test_client):

        assert len(list(get_magazine_details(999))) == 0

    def test_get_magazine_details_with_no_parameter_passed(self, test_client):
        assert len(list(get_magazine_details())) == 0

    invalid_magazine_id_input = ["a", True, 1.23, None]

    @pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
    def test_get_magazine_details_with_invalid_data_types_parameters(
        self, test_client, invalid_magazine_id
    ):
        assert len(list(get_magazine_details(invalid_magazine_id))) == 0

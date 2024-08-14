import pytest
from flask import request

from application.search_page.helpers import format_search_word


# Tests for store_s_word_in_session()
class TestStoreSWordInSession:
    def test_store_s_word_in_session_when_s_word_not_in_session_and_a_request_s_word_is_provided(
        self,
        s_word_in_session,
    ):
        session_s_word = None
        request_s_word = request.args.get("search_box")
        s_word = s_word_in_session(session_s_word, request_s_word)

        assert s_word == "fotbal"

    def test_store_s_word_in_session_when_s_word_not_in_session_and_a_request_s_word_is_not_provided(
        self,
        s_word_in_session,
    ):
        session_s_word = None
        request_s_word = None
        s_word = s_word_in_session(session_s_word, request_s_word)

        assert s_word is None

    def test_store_s_word_in_session_with_s_word_alredy_stored_in_session_and_same_request_s_word_provided(
        self,
        s_word_in_session,
    ):
        request_s_word = request.args.get("search_box")
        session_s_word = s_word_in_session(None, request_s_word)
        s_word = s_word_in_session(session_s_word, request_s_word)

        assert s_word == "fotbal"

    def test_store_s_word_in_session_with_s_word_alredy_stored_in_session_and_diferent_request_s_word_provided(
        self,
        s_word_in_session,
    ):
        request_s_word = request.args.get("search_box")
        session_s_word = s_word_in_session(None, request_s_word)
        request_s_word = "tennis"
        s_word = s_word_in_session(session_s_word, request_s_word)

        assert s_word == "tennis"


# Tests for format_search_word
class TestFormatSearchWord:
    def test_format_search_word_with_one_word_as_input(self):
        formatted_s_word = format_search_word("darwin")
        assert formatted_s_word == "darwin"

    def test_format_search_word_with_one_word_as_input_and_extra_spaces_around(self):
        formatted_s_word = format_search_word("  darwin ")
        assert formatted_s_word == "darwin"

    def test_format_search_word_with_multiple_words_as_input_and_default_separator(
        self,
    ):
        formatted_s_word = format_search_word("Victor Babeș")
        assert formatted_s_word == "Victor Babeș"

        formatted_s_word = format_search_word("ala bala portocala")
        assert formatted_s_word == "ala bala portocala"

    def test_format_search_word_with_multiple_words_as_input_and_passed_separator(self):
        formatted_s_word = format_search_word("Victor Babeș", "+")
        assert formatted_s_word == "Victor+Babeș"

        formatted_s_word = format_search_word("ala bala portocala", "+")
        assert formatted_s_word == "ala+bala+portocala"

    def test_format_search_word_with_multiple_words_as_input_and_extra_spaces_around(
        self,
    ):
        formatted_s_word = format_search_word(" ala bala portocala ")
        assert formatted_s_word == "ala bala portocala"

    def test_format_search_word_with_accepted_special_characters(self):
        input = "Darwin-_.,„!?;:''"
        accepted_special_characters = "-_.,„!?;:'' "
        expected_output = "Darwin-_.,„!?;:''"

        formatted_s_word = format_search_word(
            input, accepted_special_characters=accepted_special_characters
        )
        assert formatted_s_word == expected_output

    def test_format_search_word_with_not_accepted_special_characters(self):
        input = r'Darwin"()&/\|~{}[]+='
        accepted_special_characters = "-_.,„!?;:'' "
        expected_output = "Darwin"

        formatted_s_word = format_search_word(
            input, accepted_special_characters=accepted_special_characters
        )

        assert formatted_s_word == expected_output

    @pytest.mark.parametrize(
        "input, expected",
        [
            (r'Victor<"()&/\|~{}[]+=Babes', "VictorBabes"),
            (r'Victor<"()&/\|~{}[]+= Babes', "Victor Babes"),
        ],
    )
    def test_format_search_word_with_multiple_words_with_not_accepted_special_characters(
        self, input, expected
    ):
        formatted_s_word = format_search_word(input)
        assert formatted_s_word == expected

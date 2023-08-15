import pytest
import flask_sqlalchemy
import werkzeug
from flask import request, current_app

# Tests for get_existent_magazines()
class TestGetExistentMagazines:
    def test_content_of_get_existent_magazines(self, test_client, existent_magazines):
        existent_magazine = ("Viaţa Noastră (1936-1937)", 153)
        non_existent_magazine = ("abc", 0)

        assert existent_magazine in existent_magazines
        assert non_existent_magazine not in existent_magazines

    def test_instance_of_get_existent_magazines(self, test_client, existent_magazines):
        assert isinstance(existent_magazines, flask_sqlalchemy.query.Query)

    def test_length_of_get_existent_magazines(self, test_client, existent_magazines):
        assert len(list(existent_magazines)) == 132


# Tests for get_magazine_name()
class TestGetMagazineName:
    def test_get_magazine_name_with_existent_magazine_id(
        self, test_client, magazine_name
    ):
        test_magazine = "Buletinul eugenic şi biopolitic (1927-1947)"

        assert test_magazine == magazine_name(33)
        assert test_magazine == magazine_name("33")

    def test_get_magazine_name_with_non_existent_magazine_id(
        self, test_client, magazine_name
    ):
        assert magazine_name(999) is None
        assert magazine_name("999") is None

    def test_get_magazine_name_with_no_parameter_passed(
        self, test_client, magazine_name
    ):
        assert magazine_name() is None

    invalid_magazine_id_input = ["a", True, 1.23, None]

    @pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
    def test_get_magazine_name_with_invalid_data_types_parameters(
        self, test_client, magazine_name, invalid_magazine_id
    ):
        assert magazine_name(invalid_magazine_id) is None


# Tests for get_magazine_details()
class TestGetMagazineDetails:
    @pytest.mark.parametrize("magazine_id", [13, "13"])
    def test_get_magazine_details_with_existent_magazine_id(
        self, test_client, magazine_details, magazine_id
    ):
        test_magazine_details = [("ANUL 1 1868", 24, 759), ("ANUL 2 1871", 2, 72)]

        for index, magazine_detail in enumerate(magazine_details(magazine_id)):
            assert test_magazine_details[index] == magazine_detail

    def test_get_magazine_details_with_not_existent_magazine_id(
        self, test_client, magazine_details
    ):

        assert len(list(magazine_details(999))) == 0

    def test_get_magazine_details_with_no_parameter_passed(
        self, test_client, magazine_details
    ):
        assert len(list(magazine_details())) == 0

    invalid_magazine_id_input = ["a", True, 1.23, None]

    @pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
    def test_get_magazine_details_with_invalid_data_types_parameters(
        self, test_client, magazine_details, invalid_magazine_id
    ):
        assert len(list(magazine_details(invalid_magazine_id))) == 0


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
    def test_format_search_word_with_one_word_as_input(self, test_client, format_word):

        formatted_s_word = format_word("darwin")
        assert formatted_s_word == "darwin"

    def test_format_search_word_with_multiple_words_as_input_and_default_separator(
        self, test_client, format_word
    ):

        formatted_s_word = format_word("Victor Babeș")
        assert formatted_s_word == "Victor Babeș"

        formatted_s_word = format_word("ala bala portocala")
        assert formatted_s_word == "ala bala portocala"

    def test_format_search_word_with_multiple_words_as_input_and_passed_separator(
        self, test_client, format_word
    ):

        formatted_s_word = format_word("Victor Babeș", "+")
        assert formatted_s_word == "Victor+Babeș"

        formatted_s_word = format_word("ala bala portocala", "+")
        assert formatted_s_word == "ala+bala+portocala"


# Tests for get_distinct_magazine_names_and_count_for_searched_term
class TestGetDistinctMagazineNamesAndCountForSearchedTerm:
    def test_instance_of_get_distinct_magazine_names_and_count_for_searched_term(
        self, test_client, distinct_magazine_names_and_count_for_searched_term
    ):

        magazine_names_and_count = distinct_magazine_names_and_count_for_searched_term(
            "fotbal"
        )
        assert isinstance(magazine_names_and_count, flask_sqlalchemy.query.Query)

    def test_response_details_of_get_distinct_magazine_names_and_count_for_searched_term(
        self, test_client, distinct_magazine_names_and_count_for_searched_term
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
class TestGetDetailsForSearchedTerm:
    def test_instance_of_get_details_for_searched_term(
        self, test_client, format_word, details_for_searched_term
    ):

        s_word = format_word("Constantin Esarcu")
        details_for_searched_term = details_for_searched_term(s_word)

        assert isinstance(details_for_searched_term, flask_sqlalchemy.query.Query)

    def test_response_details_of_get_details_for_searched_term(
        self, test_client, format_word, details_for_searched_term
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


# Tests for get_details_for_searched_term_for_specific_magazine
class TestGetDetailsForSearchedTermForSpecificMagazine:
    def test_instance_of_get_details_for_searched_term_for_specific_magazine(
        self,
        test_client,
        format_word,
        details_for_searched_term,
        details_for_searched_term_for_specific_magazine,
    ):

        s_word = format_word("Constantin Esarcu")
        details_for_searched_term = details_for_searched_term(s_word)
        magazine_filter = "Tribuna poporului(1897-1912)"
        details_for_searched_term_specific_magazine = (
            details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        assert isinstance(
            details_for_searched_term_specific_magazine, flask_sqlalchemy.query.Query
        )

    def test_response_details_of_get_details_for_searched_term_for_specific_magazine(
        self,
        test_client,
        format_word,
        details_for_searched_term,
        details_for_searched_term_for_specific_magazine,
    ):

        s_word = format_word("Constantin Esarcu")
        details_for_searched_term = details_for_searched_term(s_word)
        magazine_filter = "Tribuna poporului(1897-1912)"
        details_for_searched_term_specific_magazine = (
            details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        for row in details_for_searched_term_specific_magazine:
            assert len(row) == 6

        for (
            name,
            year,
            number,
            page,
            link,
            rowid,
        ) in details_for_searched_term_specific_magazine:
            assert isinstance(name, str)
            assert isinstance(year, str)
            assert isinstance(number, str)
            assert isinstance(page, int)
            assert isinstance(link, str)
            assert isinstance(rowid, int)

    def test_filtering_works_for_get_details_for_searched_term_for_specific_magazine(
        self,
        test_client,
        format_word,
        details_for_searched_term,
        details_for_searched_term_for_specific_magazine,
    ):

        s_word = format_word("Constantin Esarcu")
        details_for_searched_term = details_for_searched_term(s_word)
        magazine_filter = "Gazeta de Transilvania (1838-1914)"
        details_for_searched_term_specific_magazine = (
            details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        for row in details_for_searched_term_specific_magazine:
            assert row[0] == magazine_filter


# Tests for paginate_results
class TestPaginateResults:
    def test_instance_of_paginate_results(
        self, test_client, format_word, details_for_searched_term, paginate
    ):

        s_word = format_word("Victor Babeș")
        details_for_searched_term = details_for_searched_term(s_word)
        page = 1
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False
        paginated_details_for_searched_word = paginate(
            details_for_searched_term, page, per_page, error_out
        )

        assert isinstance(
            paginated_details_for_searched_word,
            flask_sqlalchemy.pagination.QueryPagination,
        )

    pages = [1, 23]

    @pytest.mark.parametrize("pages", pages)
    def test_paginate_results_returns_correct_page(
        self, test_client, format_word, details_for_searched_term, paginate, pages
    ):

        s_word = format_word("Victor Babeș")
        details_for_searched_term = details_for_searched_term(s_word)
        page = pages
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False
        paginated_details_for_searched_word = paginate(
            details_for_searched_term, page, per_page, error_out
        )

        assert paginated_details_for_searched_word.page == page

    results_per_page = [1, 10, 11, 200]

    @pytest.mark.parametrize("per_page", results_per_page)
    def test_paginate_results_returns_correct_number_of_results_per_page(
        self, test_client, format_word, details_for_searched_term, paginate, per_page
    ):

        s_word = format_word("Victor Babeș")
        details_for_searched_term = details_for_searched_term(s_word)
        page = 1
        per_page = per_page
        error_out = False
        paginated_details_for_searched_word = paginate(
            details_for_searched_term, page, per_page, error_out
        )

        assert len(paginated_details_for_searched_word.items) == per_page

    def test_paginate_results_error_out_true(
        self, test_client, format_word, details_for_searched_term, paginate
    ):

        s_word = format_word("Victor Babeș")
        details_for_searched_term = details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = True

        with pytest.raises(werkzeug.exceptions.NotFound) as err:
            paginated_details_for_searched_word = paginate(
                details_for_searched_term, page, per_page, error_out
            )
            assert paginated_details_for_searched_word == err

    def test_paginate_results_error_out_false(
        self, test_client, format_word, details_for_searched_term, paginate
    ):

        s_word = format_word("Victor Babeș")
        details_for_searched_term = details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = False

        paginated_details_for_searched_word = paginate(
            details_for_searched_term, page, per_page, error_out
        )

        assert paginated_details_for_searched_word


# Tests for replace_multiple_extra_white_spaces_with_just_one
class TestReplaceMultipleExtraWhiteSpacesWithJustOne:
    def test_replace_multiple_extra_white_spaces_with_just_one_with_multiple_consecutive_spaces(
        self, test_client, replace_white_spaces
    ):

        text = "Charles  Darwin      was        a               great  scientist"

        assert replace_white_spaces(text) == "Charles Darwin was a great scientist"

    def test_replace_multiple_extra_white_spaces_with_no_argument_passed(
        self, test_client, replace_white_spaces
    ):

        assert replace_white_spaces() == ""


# Tests for get_magazine_content_details
class TestGetMagazineContentDetails:
    def test_get_magazine_content_details_with_no_parameter_passed(
        self, test_client, magazine_content_details
    ):
        assert magazine_content_details() == ""

    invalid_parameters = ["a", False, 3.14]

    @pytest.mark.parametrize("invalid_parameters", invalid_parameters)
    def test_get_magazine_content_details_with_invalid_parameters_type(
        self, test_client, magazine_content_details, invalid_parameters
    ):
        assert magazine_content_details(invalid_parameters) == ""

    def test_get_magazine_content_details_with_inexistent_rowid(
        self, test_client, magazine_content_details
    ):
        assert magazine_content_details(0) == ""

    def test_get_magazine_content_details_with_existent_rowid(
        self, test_client, magazine_content_details
    ):
        content_details = magazine_content_details(1)

        assert len(content_details) == 5180
        assert (
            "hiar mândri de a colabora la o asemenea operă de degradare a simţului literar şi moral. Ei"
            in content_details
        )


# Tests for convert_diacritics_to_basic_latin_characters
class TestConvertDiacriticsToBasicLatinCharacters:
    def test_convert_diacritics_to_basic_latin_characters_with_no_argument_passed(
        self, convert_diacritics_to_basic_characters
    ):

        assert convert_diacritics_to_basic_characters() == ""

    invalid_parameters = [1, False, 3.14]

    @pytest.mark.parametrize("invalid_parameters", invalid_parameters)
    def test_convert_diacritics_to_basic_latin_characters_with_invalid_parameters(
        self, convert_diacritics_to_basic_characters, invalid_parameters
    ):

        assert convert_diacritics_to_basic_characters(invalid_parameters) == ""

    diacritics_to_basic_characters = [
        ("À", "A"),
        ("Á", "A"),
        ("Â", "A"),
        ("Ã", "A"),
        ("Ä", "A"),
        ("Å", "A"),
        ("Ă", "A"),
        ("à", "a"),
        ("á", "a"),
        ("â", "a"),
        ("ã", "a"),
        ("ä", "a"),
        ("ă", "a"),
        ("È", "E"),
        ("É", "E"),
        ("Ê", "E"),
        ("é", "e"),
        ("ê", "e"),
        ("è", "e"),
        ("Í", "I"),
        ("Î", "I"),
        ("í", "i"),
        ("î", "i"),
        ("Ó", "O"),
        ("Õ", "O"),
        ("Ö", "O"),
        ("Ő", "O"),
        ("ó", "o"),
        ("õ", "o"),
        ("ö", "o"),
        ("ő", "o"),
        ("Ú", "U"),
        ("Ü", "U"),
        ("Ű", "U"),
        ("ú", "u"),
        ("ü", "u"),
        ("ű", "u"),
        ("Ş", "S"),
        ("Ș", "S"),
        ("ş", "s"),
        ("ș", "s"),
        ("Ț", "T"),
        ("Ţ", "T"),
        ("ț", "t"),
        ("ţ", "t"),
    ]

    @pytest.mark.parametrize(
        "diacritics, basic_character", diacritics_to_basic_characters
    )
    def test_convert_diacritics_to_basic_latin_characters_converts_all_romanian_and_hungarian_diacritics(
        self, convert_diacritics_to_basic_characters, diacritics, basic_character
    ):
        assert convert_diacritics_to_basic_characters(diacritics) == basic_character

    words_with_diacritics_to_words_without_diacritics = [
        ("árvíztűrő tükörfúrógép", "arvizturo tukorfurogep"),
        ("ÁRVÍZTŰRŐ TÜKÖRFÚRÓGÉP", "ARVIZTURO TUKORFUROGEP"),
        ("vânătoare bărbați pietriș", "vanatoare barbati pietris"),
        ("VÂNĂTOARE BĂRBAȚI PIETRIȘ", "VANATOARE BARBATI PIETRIS"),
    ]

    @pytest.mark.parametrize(
        "words_with_diacritics, words_without_diacritics",
        words_with_diacritics_to_words_without_diacritics,
    )
    def test_convert_diacritics_to_basic_latin_characters_with_words_with_diacritics(
        self,
        convert_diacritics_to_basic_characters,
        words_with_diacritics,
        words_without_diacritics,
    ):
        assert (
            convert_diacritics_to_basic_characters(words_with_diacritics)
            == words_without_diacritics
        )

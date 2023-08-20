import pytest
import flask_sqlalchemy
import werkzeug
from flask import request, current_app

from application.home.logic import (
    get_existent_magazines,
    get_magazine_name,
    get_magazine_details,
)

from application.search_page.logic import (
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
    get_previews_for_page_id,
    add_html_tags_around_preview_string_parantheses,
)

# Tests for get_existent_magazines()
class TestGetExistentMagazines:
    def test_content_of_get_existent_magazines(self, test_client):
        existent_magazine = ("Viaţa Noastră (1936-1937)", 153)
        non_existent_magazine = ("abc", 0)

        assert existent_magazine in get_existent_magazines()
        assert non_existent_magazine not in get_existent_magazines()

    def test_instance_of_get_existent_magazines(self, test_client):
        assert isinstance(get_existent_magazines(), flask_sqlalchemy.query.Query)

    def test_length_of_get_existent_magazines(self, test_client):
        assert len(list(get_existent_magazines())) == 132


# Tests for get_magazine_name()
class TestGetMagazineName:
    def test_get_magazine_name_with_existent_magazine_id(self, test_client):
        test_magazine = "Buletinul eugenic şi biopolitic (1927-1947)"

        assert test_magazine == get_magazine_name(33)
        assert test_magazine == get_magazine_name("33")

    def test_get_magazine_name_with_non_existent_magazine_id(self, test_client):
        assert get_magazine_name(999) is None
        assert get_magazine_name("999") is None

    def test_get_magazine_name_with_no_parameter_passed(self, test_client):
        assert get_magazine_name() is None

    invalid_magazine_id_input = ["a", True, 1.23, None]

    @pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
    def test_get_magazine_name_with_invalid_data_types_parameters(
        self, test_client, invalid_magazine_id
    ):
        assert get_magazine_name(invalid_magazine_id) is None


# Tests for get_magazine_details()
class TestGetMagazineDetails:
    @pytest.mark.parametrize("magazine_id", [13, "13"])
    def test_get_magazine_details_with_existent_magazine_id(
        self, test_client, magazine_id
    ):
        test_magazine_details = [("ANUL 1 1868", 24, 759), ("ANUL 2 1871", 2, 72)]

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


# Tests for get_distinct_magazine_names_and_count_for_searched_term
class TestGetDistinctMagazineNamesAndCountForSearchedTerm:
    def test_instance_of_get_distinct_magazine_names_and_count_for_searched_term(
        self, test_client
    ):

        magazine_names_and_count = (
            get_distinct_magazine_names_and_count_for_searched_term("fotbal")
        )
        assert isinstance(magazine_names_and_count, flask_sqlalchemy.query.Query)

    def test_response_details_of_get_distinct_magazine_names_and_count_for_searched_term(
        self, test_client
    ):

        magazine_names_and_count = (
            get_distinct_magazine_names_and_count_for_searched_term("fotbal")
        )

        for row in magazine_names_and_count:
            assert len(row) == 2

        for name, count in magazine_names_and_count:
            assert isinstance(name, str)
            assert isinstance(count, int)


# Tests for get_details_for_searched_term
class TestGetDetailsForSearchedTerm:
    def test_instance_of_get_details_for_searched_term(self, test_client):

        s_word = format_search_word("Constantin Esarcu")
        details_for_searched_term = get_details_for_searched_term(s_word)

        assert isinstance(details_for_searched_term, flask_sqlalchemy.query.Query)

    def test_response_details_of_get_details_for_searched_term(self, test_client):

        s_word = format_search_word("Constantin Esarcu")
        details_for_searched_term = get_details_for_searched_term(s_word)

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
class TestGetDetailsForSpecificMagazineForSearchedTerm:
    def test_instance_of_get_details_for_specific_magazinese_for_searched_term(
        self,
        test_client,
    ):

        s_word = format_search_word("Constantin Esarcu")
        details_for_searched_term = get_details_for_searched_term(s_word)
        magazine_filter = "Tribuna poporului(1897-1912)"
        details_for_searched_term_specific_magazine = (
            get_details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        assert isinstance(
            details_for_searched_term_specific_magazine, flask_sqlalchemy.query.Query
        )

    def test_response_details_of_get_details_for_specific_magazine_for_searched_term(
        self,
        test_client,
    ):

        s_word = format_search_word("Constantin Esarcu")
        details_for_searched_term = get_details_for_searched_term(s_word)
        magazine_filter = "Tribuna poporului(1897-1912)"
        details_for_searched_term_specific_magazine = (
            get_details_for_searched_term_for_specific_magazine(
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
    ):

        s_word = format_search_word("Constantin Esarcu")
        details_for_searched_term = get_details_for_searched_term(s_word)
        magazine_filter = "Gazeta de Transilvania (1838-1914)"
        details_for_searched_term_specific_magazine = (
            get_details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        for row in details_for_searched_term_specific_magazine:
            assert row[0] == magazine_filter


# Tests for paginate_results
class TestPaginateResults:
    def test_instance_of_paginate_results(self, test_client):

        s_word = format_search_word("Victor Babeș")
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 1
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False
        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert isinstance(
            paginated_details_for_searched_word,
            flask_sqlalchemy.pagination.QueryPagination,
        )

    pages = [1, 23]

    @pytest.mark.parametrize("pages", pages)
    def test_paginate_results_returns_correct_page(self, test_client, pages):

        s_word = format_search_word("Victor Babeș")
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = pages
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False
        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert paginated_details_for_searched_word.page == page

    results_per_page = [1, 10, 11, 200]

    @pytest.mark.parametrize("per_page", results_per_page)
    def test_paginate_results_returns_correct_number_of_results_per_page(
        self, test_client, per_page
    ):

        s_word = format_search_word("Victor Babeș")
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 1
        per_page = per_page
        error_out = False
        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert len(paginated_details_for_searched_word.items) == per_page

    def test_paginate_results_error_out_true(self, test_client):

        s_word = format_search_word("Victor Babeș")
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = True

        with pytest.raises(werkzeug.exceptions.NotFound) as err:
            paginated_details_for_searched_word = paginate_results(
                details_for_searched_term, page, per_page, error_out
            )
            assert paginated_details_for_searched_word == err

    def test_paginate_results_error_out_false(self, test_client):

        s_word = format_search_word("Victor Babeș")
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = False

        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert paginated_details_for_searched_word


# Tests for replace_multiple_extra_white_spaces_with_just_one
class TestReplaceMultipleExtraWhiteSpacesWithJustOne:
    def test_replace_multiple_extra_white_spaces_with_just_one_with_multiple_consecutive_spaces(
        self,
    ):

        text = "Charles  Darwin      was        a               great  scientist"

        assert (
            replace_multiple_extra_white_spaces_with_just_one(text)
            == "Charles Darwin was a great scientist"
        )

    def test_replace_multiple_extra_white_spaces_with_no_argument_passed(
        self,
    ):

        assert replace_multiple_extra_white_spaces_with_just_one() == ""


# Tests for get_magazine_content_details
class TestGetMagazineContentDetails:
    def test_get_magazine_content_details_with_no_parameter_passed(self, test_client):
        assert get_magazine_content_details() == ""

    invalid_parameters = ["a", False, 3.14]

    @pytest.mark.parametrize("invalid_parameters", invalid_parameters)
    def test_get_magazine_content_details_with_invalid_parameters_type(
        self,
        test_client,
        invalid_parameters,
    ):
        assert get_magazine_content_details(invalid_parameters) == ""

    def test_get_magazine_content_details_with_inexistent_rowid(self, test_client):
        assert get_magazine_content_details(0) == ""

    def test_get_magazine_content_details_with_existent_rowid(self, test_client):
        content_details = get_magazine_content_details(1)

        assert len(content_details) == 5180
        assert (
            "hiar mândri de a colabora la o asemenea operă de degradare a simţului literar şi moral. Ei"
            in content_details
        )


# Tests for convert_diacritics_to_basic_latin_characters
class TestConvertDiacriticsToBasicLatinCharacters:
    def test_convert_diacritics_to_basic_latin_characters_with_no_argument_passed(
        self,
    ):

        assert convert_diacritics_to_basic_latin_characters() == ""

    invalid_parameters = [1, False, 3.14]

    @pytest.mark.parametrize("invalid_parameters", invalid_parameters)
    def test_convert_diacritics_to_basic_latin_characters_with_invalid_parameters(
        self,
        invalid_parameters,
    ):

        assert convert_diacritics_to_basic_latin_characters(invalid_parameters) == ""

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
        self,
        diacritics,
        basic_character,
    ):
        assert (
            convert_diacritics_to_basic_latin_characters(diacritics) == basic_character
        )

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
        words_with_diacritics,
        words_without_diacritics,
    ):
        assert (
            convert_diacritics_to_basic_latin_characters(words_with_diacritics)
            == words_without_diacritics
        )


# Tests for get_indexes_for_highlighting_s_word
class TestGetIndexesForHighlightingSWord:
    def test_get_indexes_for_highlighting_s_word_with_a_single_letter(
        self,
    ):
        assert get_indexes_for_highlighting_s_word("a", "Ana are mere si banane") == [
            0,
            2,
            4,
            17,
            19,
        ]

    def test_get_indexes_for_highlighting_s_word_with_a_word_with_diacritics(
        self,
    ):
        s_word = "Mărţişor"
        content = (
            "cumpărând mărţişorul elaborat de Liga Apărării contra"
            + " Atacurilor Aeriene, preţul fiind de 10 lei bucata,"
            + " mărţişor ce-1 vinde cu ocazia zilei de 1 Martie 1935."
            + " Acest mărţişor, însă cu panglicuţă"
        )
        assert get_indexes_for_highlighting_s_word(s_word, content) == [10, 105, 165]


# Tests for get_distinct_s_word_variants
class TestGetDistinctSWordsVariants:
    def test_get_distinct_s_word_variants_with_term_differing_in_letter_case(
        self,
    ):
        content = "Darwin darwin Darwin DARWIN"
        s_word_string_length = 6
        indexes_for_highlighting_s_word = [0, 7, 14, 21]

        assert get_distinct_s_word_variants(
            indexes_for_highlighting_s_word, content, s_word_string_length
        ) == ["Darwin", "darwin", "DARWIN"]

    def test_get_distinct_s_word_variants_with_term_differing_in_diacritics(
        self,
    ):
        content = "Babeș Babes Babeș Babes"
        s_word_string_length = 5
        indexes_for_highlighting_s_word = [0, 6, 12, 18]

        assert get_distinct_s_word_variants(
            indexes_for_highlighting_s_word, content, s_word_string_length
        ) == ["Babeș", "Babes"]


# Tests for add_html_mark_tags_to_the_searched_term
class TestAddHtmlMarkTagsToTheSearchedTerm:
    def test_add_html_mark_tags_to_the_searched_term_with_a_single_variant(
        self,
    ):
        distinct_s_word_variants = ["Darwin"]
        content = "Charles Darwin was a great scientist"

        assert (
            add_html_mark_tags_to_the_searched_term(distinct_s_word_variants, content)
            == "Charles <mark>Darwin</mark> was a great scientist"
        )

    def test_add_html_mark_tags_to_the_searched_term_with_a_multiple_variants(
        self,
    ):
        distinct_s_word_variants = ["Babeș", "BABEȘ", "Babes"]
        content = "Different versions of Babeș name: Babeș, BABEȘ, Babes."

        assert (
            add_html_mark_tags_to_the_searched_term(distinct_s_word_variants, content)
            == "Different versions of <mark>Babeș</mark> name: <mark>Babeș</mark>, <mark>BABEȘ</mark>, <mark>Babes</mark>."
        )


# Tests for get_all_start_and_end_indexes_for_preview_substrings
class TestGetAllStartAndEndIndexesForPreviewSubstrings:
    def test_get_all_start_and_end_indexes_for_preview_substrings_with_searched_term_at_index_0(
        self,
    ):
        content = "Darwin as an emi nent geologist, whose observations"
        preview_length = 10
        s_word_string_length = len("Darwin")
        indexes = [0]

        expected_result = [[0, 16]]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )

    def test_get_all_start_and_end_indexes_for_preview_substrings_with_searched_term_at_last_index(
        self,
    ):
        content = "Publication of his journal of the vo yage made Darwin"
        preview_length = 10
        s_word_string_lenth = len("Darwin")
        indexes = [47]

        expected_result = [[indexes[0] - preview_length, len(content) + preview_length]]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_lenth, indexes
            )
            == expected_result
        )

    def test_get_all_start_and_end_indexes_for_preview_substrings_with_searched_term_in_the_middle(
        self,
    ):
        content = "Publication of his journal of the yage made Darwin famous as a popular author"
        preview_length = 10
        s_word_string_length = len("Darwin")
        indexes = [44]

        expected_result = [
            [
                indexes[0] - preview_length,
                indexes[0] + s_word_string_length + preview_length,
            ]
        ]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )

    def test_get_all_start_and_end_indexes_for_preview_substrings_with_preview_length_start_in_the_middle_of_word(
        self,
    ):
        content = "Publication of his journal of the voyage made Darwin famous as a popular author"
        preview_length = 10
        s_word_string_length = len("Darwin")
        indexes = [46]

        expected_result = [[34, indexes[0] + s_word_string_length + preview_length]]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )

    def test_get_all_start_and_end_indexes_for_preview_substrings_with_preview_length_end_in_the_middle_of_word(
        self,
    ):
        content = "Publication of his journal of the vo yage made Darwin famous popular author"
        preview_length = 10
        s_word_string_length = len("Darwin")
        indexes = [47]

        expected_result = [[indexes[0] - preview_length, 68]]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )

    def test_get_all_start_and_end_indexes_for_preview_substrings_with_multiple_indexes(
        self,
    ):
        content = (
            "Darwin as an eminent geologist, whose observations and Darwin theories"
            + " supported Charles Lyell's concept of Darwin gradual geological change. Publication"
            + " of his journal of the voyage made Darwin famous as a popular author"
        )
        preview_length = 10
        s_word_string_length = len("Darwin")
        indexes = [0, 55, 108, 188]

        expected_result = [[0, 20], [38, 80], [97, 133], [176, 204]]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )

    preview_lengths = [
        (5, [[0, 12], [51, 70], [97, 122], [183, 201]]),
        (15, [[0, 30], [38, 80], [89, 133], [172, 214]]),
        (25, [[0, 31], [31, 88], [81, 140], [161, 221]]),
        (100, [[0, 107], [0, 168], [7, 214], [89, 294]]),
        (200, [[0, 206], [0, 261], [0, 314], [0, 394]]),
    ]

    @pytest.mark.parametrize("preview_length, expected_result", preview_lengths)
    def test_get_all_start_and_end_indexes_for_preview_substrings_with_multiple_preview_length_values(
        self,
        preview_length,
        expected_result,
    ):
        content = (
            "Darwin as an eminent geologist, whose observations"
            + " and Darwin theories supported Charles Lyell's concept of Darwin gradual geological"
            + " change. Publication of his journal of the voyage made Darwin famous as a popular author"
        )
        s_word_string_length = len("Darwin")
        indexes = [0, 55, 108, 188]

        assert (
            get_all_start_and_end_indexes_for_preview_substrings(
                content, preview_length, s_word_string_length, indexes
            )
            == expected_result
        )


# Tests for merge_overlapping_preview_substrings
class TestMergeOverlappingPreviewSubstrings:
    def test_merge_overlapping_preview_substrings_with_non_overlapping_indexes(
        self,
    ):
        preview_substrings_start_end_indexes = [[0, 12], [17, 28], [36, 80]]
        expected_result = [[0, 12], [17, 28], [36, 80]]

        assert (
            merge_overlapping_preview_substrings(preview_substrings_start_end_indexes)
            == expected_result
        )

    def test_merge_overlapping_preview_substrings_with_overlapping_indexes(
        self,
    ):
        preview_substrings_start_end_indexes = [
            [0, 18],
            [17, 28],
            [95, 100],
            [96, 102],
            [103, 110],
            [103, 111],
            [112, 116],
            [116, 120],
            [121, 126],
            [124, 129],
            [128, 131],
            [130, 133],
        ]
        expected_result = [[0, 28], [95, 102], [103, 111], [112, 120], [121, 133]]

        assert (
            merge_overlapping_preview_substrings(preview_substrings_start_end_indexes)
            == expected_result
        )

    def test_merge_overlapping_preview_substrings_with_overlapping_and_non_overlapping_indexes(
        self,
    ):
        preview_substrings_start_end_indexes = [
            [0, 18],
            [17, 28],
            [29, 35],
            [36, 40],
            [42, 45],
            [42, 46],
            [47, 70],
            [71, 80],
            [112, 116],
            [116, 120],
        ]

        expected_results = [
            [0, 28],
            [29, 35],
            [36, 40],
            [42, 46],
            [47, 70],
            [71, 80],
            [112, 120],
        ]

        assert (
            merge_overlapping_preview_substrings(preview_substrings_start_end_indexes)
            == expected_results
        )


# Tests for get_preview_string
class TestGetPreviewString:
    def test_get_preview_string_with_no_added_brackets_at_the_start_or_end_of_preview_string(
        self,
    ):
        preview_substring_indexes = [[0, 30], [38, 80], [89, 133]]
        content = (
            "Darwin as an eminent geologist, whose observations and Darwin theories"
            + " supported Charles Lyell's concept of Darwin gradual geological"
        )

        expected_result = (
            "Darwin as an eminent geologist [...] observations and Darwin theories"
            + " supported [...] Lyell's concept of Darwin gradual geological"
        )

        assert get_preview_string(preview_substring_indexes, content) == expected_result

    def test_get_preview_string_with_added_bracket_at_the_end_of_preview_string(
        self,
    ):
        preview_substring_indexes = [[0, 30], [38, 80], [89, 133]]
        content = (
            "Darwin as an eminent geologist, whose observations and Darwin theories"
            + " supported Charles Lyell's concept of Darwin gradual geological change."
        )

        expected_result = (
            "Darwin as an eminent geologist [...] observations and"
            + " Darwin theories supported [...] Lyell's concept of"
            + " Darwin gradual geological [...]"
        )

        assert get_preview_string(preview_substring_indexes, content) == expected_result

    def test_get_preview_string_with_added_bracket_at_the_start_of_preview_string(
        self,
    ):
        preview_substring_indexes = [[6, 55], [63, 105], [114, 158]]
        content = (
            "as an eminent geologist. Darwin as an eminent geologist, whose observations"
            + " and Darwin theories supported Charles Lyell's concept of Darwin gradual geological"
        )

        expected_result = (
            "[...] eminent geologist. Darwin as an eminent geologist [...]"
            + " observations and Darwin theories supported [...] Lyell's"
            + " concept of Darwin gradual geological"
        )

        assert get_preview_string(preview_substring_indexes, content) == expected_result

    def test_get_preview_string_with_added_brackets_at_the_start_and_end_of_preview_string(
        self,
    ):
        preview_substring_indexes = [[6, 55], [63, 105], [114, 158]]
        content = (
            "as an eminent geologist. Darwin as an eminent geologist, whose"
            + " observations and Darwin theories supported Charles Lyell's"
            + " concept of Darwin gradual geological change"
        )

        expected_result = (
            "[...] eminent geologist. Darwin as an eminent"
            + " geologist [...] observations and Darwin theories"
            + " supported [...] Lyell's concept of Darwin gradual"
            + " geological [...]"
        )

        assert get_preview_string(preview_substring_indexes, content) == expected_result

    def test_get_preview_string_with_empty_list_passed_for_preview_substring_indexes(
        self,
    ):
        preview_substring_indexes = []
        content = "Darwin as an eminent geologist, whose observations"

        expected_result = "preview not available"

        assert get_preview_string(preview_substring_indexes, content) == expected_result


# Tests for add_html_tags_around_preview_string_parantheses
class TestAddHtmlTagsAroundPreviewStringParantheses:
    def test_add_html_tags_around_preview_string_parantheses(self):
        content = "[...] abc[...]cbd [...] bnm[...] [...]"
        expected_result = "<b><i>[...]</i></b> abc<b><i>[...]</i></b>cbd <b><i>[...]</i></b> bnm<b><i>[...]</i></b> <b><i>[...]</i></b>"

        assert (
            add_html_tags_around_preview_string_parantheses(content) == expected_result
        )


# Tests for get_previews_for_page_id
class TestGetPreviewsForPageId:
    def test_get_previews_for_page_id_length_of_response_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert len(res) == 1

    def test_get_previews_for_page_id_type_of_response_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):

        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert isinstance(res, list)
        assert isinstance(res[0][0], int)
        assert isinstance(res[0][1], str)

    def test_get_previews_for_page_id_content_of_response_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):

        (
            s_word,
            page_id,
            paginated_details_for_searched_term,
        ) = set_up_data_for_previews_for_page_id

        expected_page_id = page_id
        expected_preview_text = (
            "<b><i>[...]</i></b> două natură. Acum un an s'a făcut aci"
            + " la Ateneu, experienţa. Intr'o conferinţă de un merit real,"
            + " d. <mark>Ştefan Michăilescu</mark>, care trata despre"
            + " determinism de o dată a început să vorbească- cu mult emfas"
            + " despre teatrul românesc <b><i>[...]</i></b>"
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert res[0][0] == expected_page_id
        assert res[0][1] == expected_preview_text

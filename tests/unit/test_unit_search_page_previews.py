import pytest

from application.search_page.previews import (
    add_html_mark_tags_to_the_searched_term,
    add_html_tags_around_preview_string_parantheses,
    convert_diacritics_to_basic_latin_characters,
    get_all_start_and_end_indexes_for_preview_substrings,
    get_distinct_s_word_variants,
    get_indexes_for_highlighting_s_word,
    get_preview_string,
    merge_overlapping_preview_substrings,
    replace_multiple_extra_white_spaces_with_just_one,
)


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

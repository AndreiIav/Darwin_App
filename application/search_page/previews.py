import re

from markupsafe import Markup

from application.search_page.search_page_data_repository import (
    get_magazine_content_details,
)


def get_previews_for_page_id(
    paginated_details_for_searched_term, s_word, preview_length
):
    """
    Generate preview texts for page IDs based on provided search term.

    Args:
        paginated_details_for_searched_term
        (flask_sqlalchemy.pagination.QueryPagination): A flask_sqlalchemy
        Pagination object containing search results.
        s_word (str): The term to generate preview text around.
        preview_length (int) : The length of the preview before and after the
        search term.

    Returns: previews_for_page_id (list): A list containing pairs of
    page IDs (int) and their corresponding preview texts (str).

    This function generates preview texts for page IDs using a provided
    Flask-SQLAlchemy Pagination object (paginated_details_for_searched_term)
    and a search term (s_word).
    The generated previews are centered around the search term with the
    specified preview length.

    The function employs a series of helper functions to create these previews,
    including text processing and formatting operations.
    """

    previews_for_page_id = []

    for result in paginated_details_for_searched_term:
        page_id = result[-1]

        content = get_magazine_content_details(page_id)
        content = replace_multiple_extra_white_spaces_with_just_one(content)

        s_word_string_length = len(s_word)

        indexes_for_highlighting_s_word = get_indexes_for_highlighting_s_word(
            s_word, content
        )
        distinct_s_word_variants = get_distinct_s_word_variants(
            indexes_for_highlighting_s_word, content, s_word_string_length
        )

        preview_substrings_start_end_indexes = (
            get_all_start_and_end_indexes_for_preview_substrings(
                content,
                preview_length,
                s_word_string_length,
                indexes_for_highlighting_s_word,
            )
        )
        preview_substring_indexes = merge_overlapping_preview_substrings(
            preview_substrings_start_end_indexes
        )
        preview_string = get_preview_string(preview_substring_indexes, content)

        preview_string_with_highlighted_s_word = Markup(
            (
                add_html_tags_around_preview_string_parantheses(
                    add_html_mark_tags_to_the_searched_term(
                        distinct_s_word_variants, preview_string
                    )
                )
            )
        )

        previews_for_page_id.append([page_id, preview_string_with_highlighted_s_word])

    return previews_for_page_id


def replace_multiple_extra_white_spaces_with_just_one(text=""):
    """
    Replace multiple consecutive whitespace characters with a single space.

    Args:
        text (str): The input text string. Default is empty string: "".

    Returns:
        replaced_text (str): The modified text string with multiple consecutive
        spaces replaced by a single space.
    """

    pattern = r"\s{2,}"
    replaced_text = re.sub(pattern, " ", text)

    return replaced_text


def convert_diacritics_to_basic_latin_characters(string_to_convert=""):
    """
    Convert diacritics in a string to basic Latin characters.

    Args:
        string_to_convert (str, optional): The input string containing
        diacritics. Defaults to an empty string.

    Returns:
        converted_string (str): The input string with Romanian and Hungarian
        diacritics replaced by basic Latin
        characters, or an empty string if no argument is provided or an argument
        of invalid type is given.
    """

    if not isinstance(string_to_convert, str):
        return ""

    convert_diacritics_to_basic_latin_characters_dict = {
        192: 65,  # À -> A
        193: 65,  # Á -> A
        194: 65,  # Â -> A
        195: 65,  # Ã -> A
        196: 65,  # Ä -> A
        197: 65,  # Å -> A
        258: 65,  # Ă -> A
        224: 97,  # à -> a
        225: 97,  # á -> a
        226: 97,  # â -> a
        227: 97,  # ã -> a
        228: 97,  # ä -> a
        259: 97,  # ă -> a
        200: 69,  # È -> E
        201: 69,  # É -> E
        202: 69,  # Ê -> E
        233: 101,  # é -> e
        234: 101,  # ê -> e
        232: 101,  # è -> e
        205: 73,  # Í -> I
        206: 73,  # Î -> I
        237: 105,  # í -> i
        238: 105,  # î -> i
        211: 79,  # Ó -> O
        213: 79,  # Õ -> O
        214: 79,  # Ö -> O
        336: 79,  # Ő -> O
        243: 111,  # ó -> o
        245: 111,  # õ -> o
        246: 111,  # ö -> o
        337: 111,  # ő -> o
        218: 85,  # Ú -> U
        220: 85,  # Ü -> U
        368: 85,  # Ű -> U
        250: 117,  # ú -> u
        252: 117,  # ü -> u
        369: 117,  # ű -> u
        350: 83,  # Ş -> S
        536: 83,  # Ș -> S
        351: 115,  # ş -> s
        537: 115,  # ș -> s
        538: 84,  # Ț -> T
        354: 84,  # Ţ -> T
        539: 116,  # ț -> t
        355: 116,  # ţ -> t
    }

    converted_string = string_to_convert.translate(
        convert_diacritics_to_basic_latin_characters_dict
    )

    return converted_string


def get_indexes_for_highlighting_s_word(s_word, content):
    """
    Find all starting indices of a specified term in the given content.

    Args:
        s_word (str): The term to search for.
        content (str): The text to search within.

    Returns:
        indexes_for_highlighting_s_word (list): A list of integers representing
        the starting indexes of each occurrence of the searched term.
    """

    formatted_content_string = convert_diacritics_to_basic_latin_characters(
        content
    ).lower()
    formatted_s_word = convert_diacritics_to_basic_latin_characters(s_word).lower()
    s_word_string_length = len(s_word)

    indexes_for_highlighting_s_word = []
    find_s_word = formatted_content_string.find(formatted_s_word)

    while find_s_word > -1:
        indexes_for_highlighting_s_word.append(find_s_word)
        current_last_index = indexes_for_highlighting_s_word[-1]
        index_content_string = formatted_content_string[
            current_last_index + s_word_string_length :
        ]

        find_s_word = index_content_string.find(formatted_s_word)
        if find_s_word > -1:
            find_s_word = current_last_index + s_word_string_length + find_s_word

    return indexes_for_highlighting_s_word


def get_distinct_s_word_variants(
    indexes_for_highlighting_s_word, content, s_word_string_length
):
    """
    Find distinct versions of the searched term in the given content.

    Args:
        indexes_for_highlighting_s_word (list of int): A list of integers
        representing string indexes.
        content (str): The string in which to search for the term.
        s_word_string_length (int): The length of the searched term.

    Returns:
        distinct_s_words_variants (list of str): A list of distinct variants of
        the searched term.

    The function returns variations caused by different case letters or the use
    of diacritics for a term (i, e.: "Darwin", "darwin" or "Babeș","Babes").
    """

    distinct_s_word_variants = []

    for index in indexes_for_highlighting_s_word:
        string_to_search = content[index : index + s_word_string_length]
        if string_to_search not in distinct_s_word_variants:
            distinct_s_word_variants.append(string_to_search)

    return distinct_s_word_variants


def add_html_mark_tags_to_the_searched_term(distinct_s_word_variants, content):
    """
    Add HTML <mark> tags around every variant of a term in the content.

    Args:
        distinct_s_word_variants (list of str): A list of distinct variants for
        a term.
        content (str): The content string to modify.

    Returns:
        content (str): The modified content with HTML <mark> tags around each
        variant of the term.
    """

    while len(distinct_s_word_variants) > 0:
        word = distinct_s_word_variants.pop()
        content = content.replace(word, "<mark>" + word + "</mark>")

    return content


def add_html_tags_around_preview_string_parantheses(content):
    """
    Add HTML <b> and <i> tags around every occurrance of "[...]" in the content.

    Args:
        content (str): The content string to modify.

    Returns:
        content (str): The modified content with HTML <b> and <i> tags around
        every occurrance of "[...]" in the content.
    """

    content = content.replace("[...]", "<b><i>" + "[...]" + "</i></b>")
    return content


def get_all_start_and_end_indexes_for_preview_substrings(
    content, preview_length, s_word_string_length, indexes
):
    """
    Get start and end indexes for substrings around searched term occurrences.

    Args:
        content (str): The content string to process.
        preview_length (int): The length before and after a searched term for
        the needed substring.
        s_word_string_length (int): The length of the searched term.
        indexes (list): A list with the start indexes of searched term
        occurrences.

    Returns:
        preview_substrings_start_end_indexes (list): A list containing lists
        with start and end indexes for the substrings.

    This function accepts a content string (content) and retrieves start and end
    indexes for substrings around searched term occurrences.
    The length of each substring is determined by the provided preview_length,
    with consideration for maintaining complete words.

    Note:
        The lenght of the substring could be more or less than the set
        preview_lenght because the function will try to return substrings that
        start and end with complete words. For example, if the preview_length
        is set to 10 characters, the function will ensure that the returned
        substring includes full words and may extend beyond 10 characters if
        necessary.
    """

    preview_substrings_start_end_indexes = []
    content_length = len(content)

    for index in indexes:
        start, end = 0, 0

        if index <= preview_length:
            start = index - index
            end = index + preview_length + s_word_string_length
            while end <= content_length and content[end].isalnum():
                end += 1

        else:
            start = index - preview_length
            while start >= 0 and content[start].isalnum():
                start -= 1
            end = index + preview_length + s_word_string_length
            while end < content_length and content[end].isalnum():
                end += 1

        if not content[start].isalnum():
            start += 1

        preview_substrings_start_end_indexes.append([start, end])

    return preview_substrings_start_end_indexes


def merge_overlapping_preview_substrings(preview_substrings_start_end_indexes):
    """
    Merge overlapping intervals in a list of start and end indexes pairs.

    Args:
        preview_substrings_start_end_indexes (list): A list containing lists of
        start and end indexes pairs.

    Returns:
        preview_substrings_indexes (list): A list containing merged lists of
        start and end indexes.

    This function accepts a list (preview_substrings_start_end_indexes)
    containing lists of start and end indexes pairs. It merges overlapping
    intervals within the lists and returns a list containing the merged start
    and end index pairs. If there are no overlapping intervals, the function
    returns a list with the original lists passed.
    """

    preview_substrings_indexes = []

    pointer = 0
    while pointer <= len(preview_substrings_start_end_indexes) - 1:
        new_start = preview_substrings_start_end_indexes[pointer][0]
        new_end = preview_substrings_start_end_indexes[pointer][1]

        if pointer < len(preview_substrings_start_end_indexes) - 1:
            while (
                preview_substrings_start_end_indexes[pointer + 1][0]
                <= preview_substrings_start_end_indexes[pointer][1]
            ):
                new_end = preview_substrings_start_end_indexes[pointer + 1][1]
                pointer += 1
                if pointer == len(preview_substrings_start_end_indexes) - 1:
                    break

        interval = [new_start, new_end]
        preview_substrings_indexes.append(interval)
        pointer += 1

    return preview_substrings_indexes


def get_preview_string(preview_substrings_indexes, content):
    """
    Create a concatenated string with substrings based on provided indexes and
    delimited by " [...] ".

    Args:
        preview_substrings_indexes (list): A list containg lists of start and
        end indexes pairs.
        content (str): The text to extract the substrings from.
    Returns:
        preview_string (str): A concatenated string of substrings delimited by
        " [...] ". If preview_substrings_indexes is an empty lits,
        "preview not available" is returned.

    If the start index of the first element in preview_substrings_indexes is
    zero, "[...] " is added to the beginning of the preview_string.
    If the end index of the last element in preview_substrings_indexes is equal
    to or greater than the length of the content, " [...]" is added to the end
    of the preview_string.
    """

    content_length = len(content)
    preview_string = "preview not available"

    if preview_substrings_indexes:
        substrings = []

        for substring_indexes in preview_substrings_indexes:
            start_index, end_index = substring_indexes[0], substring_indexes[1]
            substring = content[start_index:end_index]
            substrings.append(substring)

        preview_string = " [...] ".join(substrings)

        if not (
            preview_substrings_indexes[0][0] == 0
            and preview_substrings_indexes[-1][1] >= content_length
        ):
            if (
                preview_substrings_indexes[0][0] == 0
                and preview_substrings_indexes[-1][1] < content_length
            ):
                preview_string = preview_string + " [...]"
            elif (
                preview_substrings_indexes[0][0] > 0
                and preview_substrings_indexes[-1][1] >= content_length
            ):
                preview_string = "[...] " + preview_string
            else:
                preview_string = "[...] " + preview_string + " [...]"

    return preview_string

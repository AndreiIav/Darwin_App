import re
from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContentFTS,
    db,
)
from sqlalchemy import func
from flask import session

from markupsafe import Markup


def get_details_for_searched_term(formatted_s_word):
    """
    Retrieve specific columns from multiple tables based on a provided search term.

    Args:
        formatted_s_word (str): The search term used for retrieval.

    Returns:
        all_details_for_searched_term (flask_sqlalchemy.query.Query): A Query object
        containing the retrieved results.

    This function returns a SQLAlchemy Query object that retrieves specific columns
    (Magazines.name, MagazineYear.year, MagazineNumber.magazine_number,
    MagazineNumberContentFTS.magazine_page, MagazineNumber.magazine_number_link,
    and MagazineNumberContentFTS.rowid) from multiple tables based on a provided search
    term.
    The search is performed on an FTS5 table, which enables fast text search capabilities.
    The Query object can be iterated to access the results.
    """

    all_details_for_searched_term = (
        db.session.query(
            Magazines.name,
            MagazineYear.year,
            MagazineNumber.magazine_number,
            MagazineNumberContentFTS.magazine_page,
            MagazineNumber.magazine_number_link,
            MagazineNumberContentFTS.rowid,
        )
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContentFTS,
            MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
        )
        .filter(
            MagazineNumberContentFTS.magazine_content.match(f'"{formatted_s_word}"*')
        )
    )

    return all_details_for_searched_term


def get_details_for_searched_term_for_specific_magazine(
    details_for_searched_term, magazine_filter
):
    """
    Filter a SQLAlchemy Query object based on a provided filter term.

    Args:
        details_for_searched_term (flask_sqlalchemy.query.Query): The Query object returned by the
        get_details_for_searched_term function.
        magazine_filter (str): The filter term representing Magazines.name.

    Returns:
        details_for_specific_magazine (flask_sqlalchemy.query.Query): A new Query object containing the
        filtered results.
    """

    details_for_specific_magazine = details_for_searched_term.filter(
        Magazines.name == magazine_filter
    )

    return details_for_specific_magazine


def paginate_results(details_for_searched_term, page, per_page, error_out):
    """
    Generate a SQLAlchemy Pagination object for the provided Query.

    Args:
        details_for_searched_term (flask_sqlalchemy.query.Query): The SQLAlchemy Query object to paginate.
        page (int): The page number to retrieve.
        per_page (int): The number of results to be displayed on a page.
        error_out (bool): The error flag for the error_out argument for the pagination object.

    Returns:
        flask_sqlalchemy.pagination.QueryPagination: A Pagination object representing the subset of query
        results for the requested page.
    """
    return details_for_searched_term.paginate(
        page=page, per_page=per_page, error_out=error_out
    )


def get_distinct_magazine_names_and_count_for_searched_term(formatted_s_word):
    """
    Retrieve distinct magazine names and search term counts based on the formatted_s_word.

    Args:
        formatted_s_word (str): The formatted search word obtained from format_search_word function.

    Returns:
        flask_sqlalchemy.query.Query: A Query object containing tuples of magazine names and search term counts.

    The Query object can be iterated to access the magazine names and their respective search term counts.
    """

    distinct_magazine_names_and_count_for_searched_term = (
        db.session.query(Magazines.name, func.count(Magazines.name))
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContentFTS,
            MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
        )
        .filter(
            MagazineNumberContentFTS.magazine_content.match(f'"{formatted_s_word}"*')
        )
        .group_by(Magazines.name)
    )

    return distinct_magazine_names_and_count_for_searched_term


def format_search_word(s_word, separator=" "):
    """
    Format the search word for querying.

    Args:
        s_word (str): The input search word.
        separator (str): The separator used in case there are multiple words. Default is " ".

    Returns:
        formatted_s_word (str): The formatted search word.

    This function returns the inputted search word if it is a single word, or the inputted
    search word concatenated with the separator sign if there are more than one term in s_word.
    """

    s_word_list = s_word.split()

    if len(s_word_list) == 1:
        formatted_s_word = s_word
    else:
        formatted_s_word = separator.join(s_word_list)

    return formatted_s_word


def get_magazine_content_details(page_id=0):
    """
    Retrieve the content of a magazine page from the MagazineNumberContentFTS table based on the
    provided page_id.

    Args:
        page_id (int): The rowid of the page to retrieve the content for. Defaults to 0.

    Returns:
        magazine_content_details (str): The content of the magazine page if found. If not found or
        if the parameter is of an invalid data type the string will be empty.
    """

    magazine_content_details = db.session.query(
        MagazineNumberContentFTS.magazine_content
    ).filter(MagazineNumberContentFTS.rowid == page_id)

    # Check that the Query object is not empty
    if magazine_content_details.first():
        return magazine_content_details[0][0]

    return ""


def replace_multiple_extra_white_spaces_with_just_one(text=""):

    """
    Replace multiple consecutive whitespace characters with a single space.

    Args:
        text (str): The input text string. Default is empty string: "".

    Returns:
        str: The modified text string with multiple consecutive spaces replaced by a single space.
    """

    pattern = r"\s{2,}"
    replaced_text = re.sub(pattern, " ", text)

    return replaced_text


def convert_romanian_diacritics_to_english(string_to_convert):
    """
    A function that accepts a string and returns the string with the romanian diacritics
    replaced by english characters.
    """

    convert_romanian_diacritics_to_english_dict = {
        259: 97,  # ă -> a
        226: 97,  # â -> a
        238: 105,  # î -> i
        351: 115,  # ş -> s
        537: 115,  # ș -> s
        539: 116,  # ț -> t
        355: 116,  # ţ -> t
        233: 101,  # é -> e
        234: 101,  # ê -> e
        232: 101,  # è -> e
    }

    converted_string = string_to_convert.lower().translate(
        convert_romanian_diacritics_to_english_dict
    )

    return converted_string


def get_indexes_for_highlighting_s_word(s_word, content, s_word_string_length):
    """
    A function that accepts the searched term (s_word, string) and the content of
    show_page view as string (content, string).
    It returns a list of all the start indexes (int) where the searched term is found in content.
    """

    formatted_content_string = convert_romanian_diacritics_to_english(content)
    formatted_s_word = convert_romanian_diacritics_to_english(s_word)

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


def get_distinct_s_words_variants(
    indexes_for_highlighting_s_word, content, s_word_string_length
):
    """
    A function that accepts a list of indexes (indexes_for_highlighting_s_word, int), the
    content of show_page view as string (content, string) and the length of the searched term
    (content_string_length, int).
    It returns a list of distinct versions (list of strings) (i, e.: "Darwin", "darwin" or 'Babeș',
    'babeș') of the searched term.
    """

    distinct_s_words_variants = []

    for index in indexes_for_highlighting_s_word:
        string_to_search = content[index : index + s_word_string_length]
        if string_to_search not in distinct_s_words_variants:
            distinct_s_words_variants.append(string_to_search)

    return distinct_s_words_variants


def add_html_mark_tags_to_the_searched_term(distinct_s_words_variants, content):
    """
    A function that accepts a list of distinct versions of the searched term (list of strings)
    and the content of show_page view as string (content, string).
    It returns the content of show_page view as string with <mark> tags around all versions of
    the searched term.
    """

    while len(distinct_s_words_variants) > 0:
        word = distinct_s_words_variants.pop()
        content = content.replace(word, "<mark>" + word + "</mark>")

    return content


def add_html_tags_around_preview_string_parantheses(content):

    content = content.replace("[...]", "<b><i>" + "[...]" + "</b></i>")
    return content


def get_all_start_and_end_indexes_for_preview_substrings(
    content, content_length, preview_length, s_word_string_length, indexes
):

    start, end = 0, 0
    preview_substrings_start_end_indexes = []

    for index in indexes:

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


def get_preview_string(preview_substrings_indexes, content, content_length):

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

    return "preview not available"


def get_previews_for_page_id(
    paginated_details_for_searched_term, s_word, preview_length
):

    previews_for_page_id = []

    for result in paginated_details_for_searched_term:
        page_id = result[-1]

        content = get_magazine_content_details(page_id)
        content = replace_multiple_extra_white_spaces_with_just_one(content)

        s_word_string_length = len(s_word)
        content_length = len(content)

        indexes_for_highlighting_s_word = get_indexes_for_highlighting_s_word(
            s_word, content, s_word_string_length
        )
        distinct_s_words_variants = get_distinct_s_words_variants(
            indexes_for_highlighting_s_word, content, s_word_string_length
        )

        preview_substrings_start_end_indexes = (
            get_all_start_and_end_indexes_for_preview_substrings(
                content,
                content_length,
                preview_length,
                s_word_string_length,
                indexes_for_highlighting_s_word,
            )
        )
        preview_substring_indexes = merge_overlapping_preview_substrings(
            preview_substrings_start_end_indexes
        )
        preview_string = get_preview_string(
            preview_substring_indexes, content, content_length
        )

        preview_string_with_highlighted_s_word = Markup(
            (
                add_html_tags_around_preview_string_parantheses(
                    add_html_mark_tags_to_the_searched_term(
                        distinct_s_words_variants, preview_string
                    )
                )
            )
        )

        previews_for_page_id.append([page_id, preview_string_with_highlighted_s_word])

    return previews_for_page_id


def store_s_word_in_session(session_s_word, request_s_word):
    """
    Update the value of s_word in the session with the value from the current request.

    Args:
        session_s_word (str): The current value of s_word stored in the session.
        request_s_word (str): The value of s_word from the current request.

    Returns:
        str or None: The updated value of s_word in the session, or None if no current or request
        value is provided.

    This function replaces the current value of s_word in the session with the value from the
    current request. It returns the updated value of s_word in the session, or None if no current
    value or request value is provided.
    """

    if session_s_word is None or (
        request_s_word is not None and request_s_word != session_s_word
    ):
        session["s_word"] = request_s_word

    return session.get("s_word")

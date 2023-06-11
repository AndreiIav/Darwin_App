from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContentFTS,
    db,
)
from sqlalchemy import func


def get_details_for_searched_term(formated_s_word):
    """
    A function that returns a sqlAlchemy pagination object containing the Magazines.name,
    MagazineYear.year, MagazineNumber.magazine_number, MagazineNumberContent.magazine_page,
    MagazineNumber.magazine_number_link
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
            MagazineNumberContentFTS.magazine_content.match(f'"{formated_s_word}"*')
        )
    )

    return all_details_for_searched_term


def get_details_for_searched_term_for_specific_magazine(
    details_for_searched_term, magazine_filter
):

    details_for_specific_magazine = details_for_searched_term.filter(
        Magazines.name == magazine_filter
    )

    return details_for_specific_magazine


def paginate_results(details_for_searched_term, page):
    return details_for_searched_term.paginate(page=page, per_page=10)


def get_distinct_magazine_names_and_count_for_searched_term(formated_s_word):

    distinct_magazine_names_and_count_for_searched_term = (
        db.session.query(Magazines.name, func.count(Magazines.name))
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContentFTS,
            MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
        )
        .filter(
            MagazineNumberContentFTS.magazine_content.match(f'"{formated_s_word}"*')
        )
        .group_by(Magazines.name)
    )

    return distinct_magazine_names_and_count_for_searched_term


def format_search_word(s_word):

    s_word_list = s_word.split()

    if len(s_word_list) == 1:
        formated_s_word = s_word
    else:
        formated_s_word = "+".join(s_word_list)

    return formated_s_word


def get_magazine_content_details(page_id):

    magazine_content_details = db.session.query(
        MagazineNumberContentFTS.magazine_content
    ).filter(MagazineNumberContentFTS.rowid == page_id)

    return magazine_content_details[0][0]


def get_content_string_length(s_word):
    """
    A function that accepts the searched term (s_word) and returns its length.
    """

    return len(s_word)


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


def get_indexes_for_highlighting_s_word(s_word, content, content_string_length):
    """
    A function that accepts the searched term (s_word, string) and the content of
    show_page view as string (content, string).
    It returns a list of all the start indexes (int) where the searched term is found in content.
    """

    formated_content_string = convert_romanian_diacritics_to_english(content)
    formated_s_word = convert_romanian_diacritics_to_english(s_word)

    indexes_for_highlighting_s_word = []
    find_s_word = formated_content_string.find(formated_s_word)

    while find_s_word > -1:
        indexes_for_highlighting_s_word.append(find_s_word)
        current_last_index = indexes_for_highlighting_s_word[-1]
        index_content_string = formated_content_string[
            current_last_index + content_string_length :
        ]

        find_s_word = index_content_string.find(formated_s_word)
        if find_s_word > -1:
            find_s_word = current_last_index + content_string_length + find_s_word

    return indexes_for_highlighting_s_word


def get_distinct_s_words_variants(
    indexes_for_highlighting_s_word, content, content_string_length
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
        string_to_search = content[index : index + content_string_length]
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

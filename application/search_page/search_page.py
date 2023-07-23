from flask import Blueprint
from flask import render_template, request, session, current_app
from markupsafe import Markup

from .logic import (
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    get_distinct_magazine_names_and_count_for_searched_term,
    paginate_results,
    format_search_word,
    get_magazine_content_details,
    get_indexes_for_highlighting_s_word,
    get_s_word_string_length,
    get_distinct_s_words_variants,
    add_html_mark_tags_to_the_searched_term,
    store_s_word_in_session,
    replace_multiple_extra_white_spaces_with_just_one,
    get_all_start_and_end_indexes_for_preview_substrings,
    get_length_of_content_string,
    get_preview_string,
    merge_overlapping_preview_substrings,
    add_html_tags_around_preview_string_parantheses,
)


# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/results",
)


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():

    session_s_word = session.get("s_word")
    request_s_word = request.args.get("search_box")
    request_s_word = format_search_word(request_s_word)
    s_word = store_s_word_in_session(session_s_word, request_s_word)

    formatted_s_word = format_search_word(s_word, "+")

    page = request.args.get("page", 1, type=int)

    distinct_magazines_and_count = (
        get_distinct_magazine_names_and_count_for_searched_term(
            formatted_s_word=formatted_s_word
        )
    )

    magazine_filter = request.args.get("magazine_filter")

    details_for_searched_term = get_details_for_searched_term(
        formatted_s_word=formatted_s_word
    )

    if magazine_filter:
        details_for_searched_term = get_details_for_searched_term_for_specific_magazine(
            details_for_searched_term, magazine_filter
        )

    details_for_searched_term = paginate_results(
        details_for_searched_term,
        page,
        per_page=current_app.config["RESULTS_PER_PAGE"],
        error_out=current_app.config["ERROR_OUT"],
    )

    return render_template(
        "search_page.html",
        details_for_searched_term=details_for_searched_term,
        searched_term=s_word,
        distinct_magazines_and_count=distinct_magazines_and_count,
        magazine_filter=magazine_filter,
    )


@search_page_bp.route("/show_page", methods=["GET"])
def display_magazine_content():

    s_word = session.get("s_word")
    page_id = request.args.get("page_id")
    preview_length = current_app.config["PREVIEW_SUBSTRING_LENGTH"]

    content = get_magazine_content_details(page_id)
    content = replace_multiple_extra_white_spaces_with_just_one(content)

    s_word_string_length = get_s_word_string_length(s_word)
    content_length = get_length_of_content_string(content)

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

    # content = Markup(
    #     add_html_mark_tags_to_the_searched_term(distinct_s_words_variants, content)
    # )
    # return render_template("show_page.html", content=content)

    preview_string_with_highlighted_s_word = Markup(
        add_html_tags_around_preview_string_parantheses(
            add_html_mark_tags_to_the_searched_term(
                distinct_s_words_variants, preview_string
            )
        )
    )

    return render_template(
        "show_page.html", content=preview_string_with_highlighted_s_word
    )

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
    get_content_string_length,
    get_distinct_s_words_variants,
    add_html_mark_tags_to_the_searched_term,
    store_s_word_in_session,
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

    content = get_magazine_content_details(page_id)
    content_string_length = get_content_string_length(s_word)
    indexes_for_highlighting_s_word = get_indexes_for_highlighting_s_word(
        s_word, content, content_string_length
    )
    distinct_s_words_variants = get_distinct_s_words_variants(
        indexes_for_highlighting_s_word, content, content_string_length
    )
    content = Markup(
        add_html_mark_tags_to_the_searched_term(distinct_s_words_variants, content)
    )

    return render_template("show_page.html", content=content)

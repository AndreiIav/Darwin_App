from flask import Blueprint, current_app, render_template, request, session

from application import cache
from application.search_page.helpers import format_search_word, store_s_word_in_session
from application.search_page.previews import get_previews_for_page_id
from application.search_page.search_page_data_repository import (
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    get_distinct_magazine_names_and_count_for_searched_term,
    paginate_results,
)

# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/results",
)

"""
Blueprint: search_page_bp
This blueprint handles the display of the search results.
"""


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():
    session_s_word = session.get("s_word")
    request_s_word = request.args.get("search_box")

    current_app.logger.info(
        "Calling the search_for_term() function with search_box"
        f" parameter: {request.args.get('search_box')}"
    )

    accepted_special_characters = current_app.config["ACCEPTED_FTS5_SPECIAL_CHARACTERS"]
    request_s_word = format_search_word(
        request_s_word, accepted_special_characters=accepted_special_characters
    )

    current_app.logger.info(f"Formatted search_box parameter to: {request_s_word}")

    s_word = store_s_word_in_session(session_s_word, request_s_word)
    if len(s_word) < 4 or len(s_word) > 200:
        current_app.logger.info(
            "Displaying no_results_found page because s_word"
            f" length is: {len(s_word)}"
        )
        return render_template("no_results_found.html", not_minimum_s_word_length=True)

    preview_length = current_app.config["PREVIEW_SUBSTRING_LENGTH"]
    page = request.args.get("page", 1, type=int)

    current_app.logger.info(f"Displaying /search page: {page}")

    formatted_s_word = format_search_word(
        s_word, separator="+", accepted_special_characters=accepted_special_characters
    )

    current_app.logger.info(f"Formatted s_word to: {formatted_s_word}")

    magazine_filter = request.args.get("magazine_filter")

    details_for_searched_term = get_details_for_searched_term(
        formatted_s_word=formatted_s_word
    )

    distinct_magazines_and_count_cache_key = (
        f"{formatted_s_word}_distinct_magazines_count"
    )
    if cache.has(distinct_magazines_and_count_cache_key):
        distinct_magazines_and_count = cache.get(distinct_magazines_and_count_cache_key)
    else:
        # cast Query object to list to make possible to add to cache
        distinct_magazines_and_count = list(
            get_distinct_magazine_names_and_count_for_searched_term(
                details_for_searched_term=details_for_searched_term
            )
        )
        cache.add(distinct_magazines_and_count_cache_key, distinct_magazines_and_count)

    # count the lenght of the entire result set only if a magazine_filter
    # doesn't exists
    if not magazine_filter:
        if cache.has(formatted_s_word):
            details_for_searched_term_length = cache.get(formatted_s_word)
        else:
            details_for_searched_term_length = details_for_searched_term.count()
            cache.add(formatted_s_word, details_for_searched_term_length)

        if details_for_searched_term_length == 0:
            current_app.logger.info(
                "Displaying no_results_found page because s_word"
                f" was not found: {s_word}"
            )
            return render_template("no_results_found.html", searched_term=s_word)

    else:
        current_app.logger.info(f"magazine_filter set to: {magazine_filter}")
        details_for_searched_term = get_details_for_searched_term_for_specific_magazine(
            details_for_searched_term, magazine_filter
        )

        magazine_filter_cache_key = f"{magazine_filter}_{request_s_word}"
        if cache.has(magazine_filter_cache_key):
            details_for_searched_term_length = cache.get(magazine_filter_cache_key)
        else:
            details_for_searched_term_length = details_for_searched_term.count()
            cache.add(magazine_filter_cache_key, details_for_searched_term_length)

    details_for_searched_term = paginate_results(
        details_for_searched_term,
        page,
        per_page=current_app.config["RESULTS_PER_PAGE"],
        error_out=current_app.config["ERROR_OUT"],
    )

    previews = get_previews_for_page_id(
        details_for_searched_term, s_word, preview_length
    )

    return render_template(
        "search_page.html",
        details_for_searched_term=details_for_searched_term,
        details_for_searched_term_length=details_for_searched_term_length,
        searched_term=s_word,
        distinct_magazines_and_count=distinct_magazines_and_count,
        magazine_filter=magazine_filter,
        previews=previews,
    )

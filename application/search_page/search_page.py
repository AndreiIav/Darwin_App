from flask import Blueprint, current_app, render_template, request, session

from application.search_page.logic import (
    format_search_word,
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    get_distinct_magazine_names_and_count_for_searched_term,
    get_previews_for_page_id,
    paginate_results,
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

    details_for_searched_term = get_details_for_searched_term(
        formatted_s_word=formatted_s_word
    )
    if len(list(details_for_searched_term)) == 0:
        current_app.logger.info(
            "Displaying no_results_found page because s_word"
            f" was not found: {s_word}"
        )
        return render_template("no_results_found.html", searched_term=s_word)

    distinct_magazines_and_count = (
        get_distinct_magazine_names_and_count_for_searched_term(
            details_for_searched_term=details_for_searched_term
        )
    )

    magazine_filter = request.args.get("magazine_filter")

    if magazine_filter:
        current_app.logger.info(f"magazine_filter set to: {magazine_filter}")
        details_for_searched_term = get_details_for_searched_term_for_specific_magazine(
            details_for_searched_term, magazine_filter
        )

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
        searched_term=s_word,
        distinct_magazines_and_count=distinct_magazines_and_count,
        magazine_filter=magazine_filter,
        previews=previews,
    )

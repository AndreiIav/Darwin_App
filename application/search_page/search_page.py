from flask import Blueprint
from flask import render_template, request, session, current_app, abort
from application.search_page.logic import (
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    get_distinct_magazine_names_and_count_for_searched_term,
    paginate_results,
    format_search_word,
    store_s_word_in_session,
    get_previews_for_page_id,
    check_characters_that_break_sqlalchemy_query,
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
    if len(s_word) < 4:
        return render_template("no_results_found.html", not_minimum_s_word_length=True)

    preview_length = current_app.config["PREVIEW_SUBSTRING_LENGTH"]
    page = request.args.get("page", 1, type=int)

    formatted_s_word = format_search_word(s_word, "+")

    # check if the input contains characters that break the fts
    # query (like: a single double quote(i.e., 'iulia"'))
    if check_characters_that_break_sqlalchemy_query(formatted_s_word):
        abort(422)

    distinct_magazines_and_count = (
        get_distinct_magazine_names_and_count_for_searched_term(
            formatted_s_word=formatted_s_word
        )
    )

    details_for_searched_term = get_details_for_searched_term(
        formatted_s_word=formatted_s_word
    )

    if len(list(details_for_searched_term)) == 0:
        return render_template("no_results_found.html", searched_term=s_word)

    magazine_filter = request.args.get("magazine_filter")

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

from flask import Blueprint
from flask import render_template, request, session

from .logic import (
    get_details_for_searched_term,
    get_distinct_magazine_names_and_count_for_searched_term,
    format_search_word,
    get_magazine_content_details,
)


# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp", __name__, template_folder="templates", static_folder="static"
)


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():

    if session.get("s_word") is None or (
        request.args.get("search_box") is not None
        and request.args.get("search_box") != session.get("s_word")
    ):
        session["s_word"] = request.args.get("search_box")
    s_word = session.get("s_word")

    formated_s_word = format_search_word(s_word)

    page = request.args.get("page", 1, type=int)

    magazine_filter = request.args.get("magazine_filter")

    # Returns a pagination object
    result_list = get_details_for_searched_term(
        formated_s_word=formated_s_word, page=page, magazine_filter=magazine_filter
    )

    distinct_magazines = get_distinct_magazine_names_and_count_for_searched_term(
        formated_s_word=formated_s_word
    )

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        distinct_magazines=distinct_magazines,
        magazine_filter=magazine_filter,
    )


@search_page_bp.route("/show_page", methods=["GET"])
def display_magazine_content():

    page_id = request.args.get("page_id")

    content = get_magazine_content_details(page_id)

    return content

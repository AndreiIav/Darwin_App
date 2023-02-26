from flask import Blueprint
from flask import render_template, request, session

from .logic import (
    get_json_details_for_searched_term,
    get_distinct_magazine_names_and_count_for_searched_term,
)


# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp", __name__, template_folder="templates", static_folder="static"
)


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():

    s_word = request.args.get("search_box")

    if session.get("s_word") is None or (
        s_word is not None and s_word != session.get("s_word")
    ):
        session["s_word"] = s_word
    s_word = session.get("s_word")

    page = request.args.get("page", 1, type=int)

    if request.args.get("magazine_filter") is None:
        magazine_filter = None
    else:
        magazine_filter = request.args.get("magazine_filter")

    # Returns a pagination object
    result_list = get_json_details_for_searched_term(
        s_word=s_word, page=page, magazine_filter=magazine_filter
    )

    distinct_magazines = get_distinct_magazine_names_and_count_for_searched_term(
        s_word=s_word
    )

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        distinct_magazines=distinct_magazines,
    )

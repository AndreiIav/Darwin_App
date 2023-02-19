from flask import Blueprint
from flask import render_template, request

from .logic import (
    get_json_details_for_searched_term,
    get_distinct_magazine_names_for_searched_term,
)


# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp", __name__, template_folder="templates", static_folder="static"
)


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():

    s_word = request.args.get("search_box")
    page = request.args.get("page", 1, type=int)

    # Returns a pagination object
    result_list = get_json_details_for_searched_term(s_word=s_word, page=page)

    distinct_magazines = get_distinct_magazine_names_for_searched_term(s_word=s_word)

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        distinct_magazines=distinct_magazines,
    )

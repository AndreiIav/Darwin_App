from flask import Blueprint
from flask import render_template, request

from .logic import get_json_details_for_searched_term


# Blueprint configuration
search_page_bp = Blueprint(
    "search_page_bp", __name__, template_folder="templates", static_folder="static"
)


@search_page_bp.route("/search", methods=["GET"])
def search_for_term():

    s_word = request.args["search_box"]

    result_list = get_json_details_for_searched_term(s_word=s_word)
    results_count = len(result_list)

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        results_count=results_count,
        # search_form=search_form,
    )

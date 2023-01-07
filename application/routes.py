from flask import current_app as app
from flask import render_template, request, redirect, url_for

from .forms import SearchForm
from .logic import get_json_details_for_searched_term, get_existent_magazines


@app.route("/", methods=["GET", "POST"])
def search_form():
    search_form = SearchForm()
    existent_magazines = get_existent_magazines()

    if search_form.validate_on_submit():
        return redirect(url_for("search_for_term"))

    return render_template(
        "home_page.html", search_form=search_form, existent_magazines=existent_magazines
    )


@app.route("/search", methods=["GET"])
def search_for_term():

    s_word = request.args["search_box"]

    result_list = get_json_details_for_searched_term(s_word=s_word)
    results_count = len(result_list)

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        results_count=results_count,
        search_form=search_form,
    )

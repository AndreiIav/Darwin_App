from flask import current_app as app
from flask import render_template, request

from .forms import SearchForm
from .logic import get_json_details_for_searched_term


@app.route("/")
def search_form():
    search_form = SearchForm()
    return render_template("home_page.html", search_form=search_form)


@app.route("/search", methods=["GET", "POST"])
def search_for_term():

    search_form = SearchForm()

    if request.method == "POST":

        s_word = search_form.search_box.data
        result_list = get_json_details_for_searched_term(s_word=s_word)
        results_count = len(result_list)

        return render_template(
            "search_page.html",
            result_list=result_list,
            searched_term=s_word,
            results_count=results_count,
            search_form=search_form,
        )

    return render_template("home_page.html", search_form=search_form)

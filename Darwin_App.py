from flask import Flask, render_template, request, make_response
from logic import get_json_details_for_searched_term


app = Flask(__name__)


@app.route("/")
def search_page():
    return render_template("base.html")


@app.route("/search", methods=["GET", "POST"])
def search_for_term():

    if request.method == "GET":
        return render_template("base.html")

    s_word = request.form.get("search_term", "default")
    result_list = get_json_details_for_searched_term(s_word=s_word)
    results_count = len(result_list)

    return render_template(
        "search_page.html",
        result_list=result_list,
        searched_term=s_word,
        results_count=results_count,
    )

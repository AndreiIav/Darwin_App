from flask import Flask, render_template, request, make_response
from logic import get_json_details_for_searched_term


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def search_page():
    if request.method == "GET":
        return render_template("search_page.html")
    if request.method == "POST":
        s_word = request.form.get("search_term", "default")

        headers = {"Content-Type": "application/json"}
        result_list = get_json_details_for_searched_term(s_word=s_word)

        return make_response(result_list, 200, headers)

from flask import Flask, render_template, request, make_response
from logic import get_json_details_for_searched_term


app = Flask(__name__)


@app.route("/")
def search_page():
    return render_template("search_page.html")


@app.route("/search", methods=["POST"])
def search_for_term():

    s_word = request.form.get("search_term", "default")

    headers = {"Content-Type": "application/json"}
    result_list = get_json_details_for_searched_term(s_word=s_word)

    return make_response(result_list, 200, headers)

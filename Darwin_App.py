from flask import Flask, render_template, request, make_response
from logic import get_count, get_details_for_searched_term


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def search_page():
    if request.method == "GET":
        return render_template("search_page.html")
    if request.method == "POST":
        s_word = request.form.get("search_term", "default")

        headers = {"Content-Type": "application/json"}
        result_list = get_details_for_searched_term(s_word=s_word)

        response = []
        for res in result_list:

            partial_values = {}
            partial_values["magazine_name"] = res[0]
            partial_values["magazine_year"] = res[1]
            partial_values["magazine_number"] = res[2]
            partial_values["page"] = res[3]
            partial_values["link"] = res[4]

            response.append(partial_values)

        return make_response(response, 200, headers)

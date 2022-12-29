from flask import Flask, render_template, request
from os import path
from pathlib import Path

# from logic import get_json_details_for_searched_term
# from forms import SearchForm


def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile(path.join(Path.cwd(), "config.py"))

    from . import db

    db.init_app(app)

    from . import logic
    from . import forms

    @app.route("/")
    def search_page():
        search_form = forms.SearchForm()
        return render_template("base.html", search_form=search_form)

    @app.route("/search", methods=["GET", "POST"])
    def search_for_term():

        search_form = forms.SearchForm()

        if request.method == "POST":

            s_word = search_form.search_box.data
            result_list = logic.get_json_details_for_searched_term(s_word=s_word)
            results_count = len(result_list)

            return render_template(
                "search_page.html",
                result_list=result_list,
                searched_term=s_word,
                results_count=results_count,
                search_form=search_form,
            )

        return render_template("base.html", search_form=search_form)

    return app

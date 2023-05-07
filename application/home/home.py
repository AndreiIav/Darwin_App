from flask import Blueprint, request

from flask import render_template, redirect, url_for

from application.forms import SearchForm
from .logic import get_existent_magazines


# Blueprint Configuration
home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static"
)


@home_bp.route("/", methods=["GET"])
def search_form():
    search_form = SearchForm()

    existent_magazines = get_existent_magazines()

    if search_form.validate_on_submit():
        return redirect(url_for("search_for_term"))

    return render_template(
        "home_page.html",
        search_form=search_form,
        existent_magazines=existent_magazines,
    )

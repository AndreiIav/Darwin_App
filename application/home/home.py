from flask import Blueprint, request, render_template, redirect, url_for, abort
from application.forms import SearchForm
from application.home.logic import (
    get_existent_magazines,
    get_magazine_details,
    get_magazine_name,
)


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


@home_bp.route("/magazine_details")
def show_magazine_details():

    magazine_id = request.args.get("magazine_id")
    magazine_name = get_magazine_name(magazine_id)

    if magazine_name is None:
        abort(404)

    magazine_details = get_magazine_details(magazine_id)

    return render_template(
        "magazine_details.html",
        magazine_name=magazine_name,
        magazine_details=magazine_details,
    )

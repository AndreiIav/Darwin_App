from flask import Blueprint, request, render_template, abort, current_app

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

    current_app.logger.info("Calling the search_form() function")

    search_form = SearchForm()

    existent_magazines = get_existent_magazines()
    placeholder_text_for_search_bar = (
        "the search term can have at least 4"
        + " characters and at most 200 and can be composed of multiple words"
    )

    return render_template(
        "home_page.html",
        search_form=search_form,
        existent_magazines=existent_magazines,
        placeholder_text_for_search_bar=placeholder_text_for_search_bar,
    )


@home_bp.route("/magazine_details")
def show_magazine_details():

    current_app.logger.info(
        "Calling the show_magazine_details() function"
        f" with parameter: {request.args.get('magazine_id')}"
    )

    try:
        magazine_id = int(request.args.get("magazine_id"))
    except ValueError:
        current_app.logger.error(
            "Aborted show_magazine_details() function with ValueError error"
            f" due to incorrect parameter: {request.args.get('magazine_id')}"
        )
        abort(404)
    except TypeError:
        current_app.logger.error(
            "Aborted show_magazine_details() function with TypeError error"
            f" due to incorrect parameter: {request.args.get('magazine_id')}"
        )
        abort(404)

    magazine_name = get_magazine_name(magazine_id)

    if magazine_name is None:
        current_app.logger.error(
            "Aborted show_magazine_details() function becuase magazine_name was"
            f" not found for parameter: {request.args.get('magazine_id')}"
        )
        abort(404)

    magazine_details = get_magazine_details(magazine_id)
    current_app.logger.info(
        f"Displaying the /magazine_details page for magazine_name: {magazine_name}"
    )

    return render_template(
        "magazine_details.html",
        magazine_name=magazine_name,
        magazine_details=magazine_details,
    )


@home_bp.route("/contact")
def show_contact_page():
    current_app.logger.info("Calling the show_contact_page() function")
    return render_template("contact.html")


@home_bp.route("/about")
def show_about_page():
    current_app.logger.info("Calling the show_about_page() function")
    return render_template("about.html")

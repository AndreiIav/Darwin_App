from flask_wtf import FlaskForm
from wtforms import StringField  # field types
from wtforms.validators import DataRequired, Length  # validators


class SearchForm(FlaskForm):
    search_box = StringField(
        "Search Box",
        [
            DataRequired(),
            Length(
                min=4,
                max=200,
                message=(
                    "The searched term must be greater than 3 characters and lower than 200."
                ),
            ),
        ],
    )

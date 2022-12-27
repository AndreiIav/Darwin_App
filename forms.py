from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  # field types
from wtforms.validators import DataRequired, Length  # validators


class SearchForm(FlaskForm):

    search_box = StringField(
        "Search Box",
        [
            DataRequired(),
            Length(
                min=4, message=("The searched term must be greater than 3 characters.")
            ),
        ],
    )
    submit = SubmitField("Search")

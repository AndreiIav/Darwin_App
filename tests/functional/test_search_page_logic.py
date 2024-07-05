import pytest
from flask import current_app
import flask_sqlalchemy
import werkzeug

from application.search_page.logic import (
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    paginate_results,
    get_previews_for_page_id,
)


# Tests for get_details_for_searched_term_for_specific_magazine
class TestGetDetailsForSpecificMagazineForSearchedTerm:
    def test_instance_of_get_details_for_specific_magazinese_for_searched_term(
        self,
        test_client,
    ):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be filtered
        details_for_searched_term = get_details_for_searched_term(s_word)
        magazine_filter = "Albina (1866-1876)"

        details_for_searched_term_specific_magazine = (
            get_details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        assert isinstance(
            details_for_searched_term_specific_magazine, flask_sqlalchemy.query.Query
        )

    def test_filtering_works_for_get_details_for_searched_term_for_specific_magazine(
        self,
        test_client,
    ):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be filtered
        details_for_searched_term = get_details_for_searched_term(s_word)
        magazine_filter = "Albina (1866-1876)"

        details_for_searched_term_for_specific_magazine = (
            get_details_for_searched_term_for_specific_magazine(
                details_for_searched_term, magazine_filter
            )
        )

        assert len(list(details_for_searched_term_for_specific_magazine)) == 26

        for row in details_for_searched_term_for_specific_magazine:
            assert row[0] == magazine_filter


# Tests for paginate_results
class TestPaginateResults:
    def test_type_of_paginate_results(self, test_client):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be paginated
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 1
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False

        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert isinstance(
            paginated_details_for_searched_word,
            flask_sqlalchemy.pagination.QueryPagination,
        )

    pages = [1, 22]

    @pytest.mark.parametrize("pages", pages)
    def test_paginate_results_returns_correct_page(self, test_client, pages):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be paginated
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = pages
        per_page = current_app.config["RESULTS_PER_PAGE"]
        error_out = False

        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert paginated_details_for_searched_word.page == page

    results_per_page = [1, 10, 11, 200]

    @pytest.mark.parametrize("per_page", results_per_page)
    def test_paginate_results_returns_correct_number_of_results_per_page(
        self, test_client, per_page
    ):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be paginated
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 1
        per_page = per_page
        error_out = False

        paginated_details_for_searched_word = paginate_results(
            details_for_searched_term, page, per_page, error_out
        )

        assert len(paginated_details_for_searched_word.items) == per_page

    def test_paginate_results_error_out_true_not_existing_page(self, test_client):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object to be paginated
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = True

        with pytest.raises(werkzeug.exceptions.NotFound) as err:
            paginate_results(details_for_searched_term, page, per_page, error_out)

        assert "404 Not Found" in str(err.value)

    def test_paginate_results_error_out_false_not_existing_page(self, test_client):
        s_word = "Bucuresti"
        details_for_searched_term = get_details_for_searched_term(s_word)
        page = 2000
        per_page = 10
        error_out = False

        paginate_results(details_for_searched_term, page, per_page, error_out)


# Tests for get_previews_for_page_id
class TestGetPreviewsForPageId:
    def test_get_previews_for_page_id_length_of_response_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        print(res)
        assert len(res) == 1

    def test_get_previews_for_page_id_response_type_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert isinstance(res, list)
        assert isinstance(res[0][0], int)
        assert isinstance(res[0][1], str)

    def test_get_previews_for_page_id_response_content_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        (
            s_word,
            page_id,
            paginated_details_for_searched_term,
        ) = set_up_data_for_previews_for_page_id

        expected_page_id = page_id
        expected_preview_text = (
            "<b><i>[...]</i></b> unchiu Andrei; la ce mulţimea anca prorupse in"
            + " se traiésca entusiastice pentru fostulu loru ablegatu"
            + " <mark>Andrei Mocioni</mark>. In satulu Silha bravulu"
            + " invetiatoriu co-munalu Constantinu Torna, cu tenerimea"
            + " sco-láfra, enca intona <b><i>[...]</i></b>"
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert res[0][0] == expected_page_id
        assert res[0][1] == expected_preview_text

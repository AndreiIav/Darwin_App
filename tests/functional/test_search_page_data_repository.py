import flask_sqlalchemy
import pytest
import werkzeug
from flask import current_app

from application.search_page.search_page_data_repository import (
    get_details_for_searched_term,
    get_details_for_searched_term_for_specific_magazine,
    get_distinct_magazine_names_and_count_for_searched_term,
    paginate_results,
)


# Tests for get_details_for_searched_term
class TestGetDetailsForSearchedTerm:
    def test_get_details_for_searched_term_gets_correct_data(self, test_client):
        s_word = "fotbal"
        expected_magazine_name = "Amicul Şcoalei (1925-1935)"
        expected_year = "ANUL 1930"
        expected_number = "Nr.23-24"
        expected_page = 8
        expected_link = "https://documente.bcucluj.ro/web/bibdigit/periodice/amiculscoalei/1930/BCUCLUJ_FP_279091_1930_006_023_024.pdf"
        expected_rowid = 10708

        details_for_searched_term = get_details_for_searched_term(s_word)

        for name, year, number, page, link, rowid in details_for_searched_term:
            assert name == expected_magazine_name
            assert year == expected_year
            assert number == expected_number
            assert page == expected_page
            assert link == expected_link
            assert rowid == expected_rowid

    def test_type_of_get_details_for_searched_term(self, test_client):
        s_word = "fotbal"
        details_for_searched_term = get_details_for_searched_term(s_word)

        assert isinstance(details_for_searched_term, flask_sqlalchemy.query.Query)

    def test_response_details_of_get_details_for_searched_term(self, test_client):
        s_word = "fotbal"
        details_for_searched_term = get_details_for_searched_term(s_word)

        assert len(list(details_for_searched_term)) == 1

        for row in details_for_searched_term:
            assert len(row) == 6

        for name, year, number, page, link, rowid in details_for_searched_term:
            assert isinstance(name, str)
            assert isinstance(year, str)
            assert isinstance(number, str)
            assert isinstance(page, int)
            assert isinstance(link, str)
            assert isinstance(rowid, int)


# Tests for get_distinct_magazine_names_and_count_for_searched_term
class TestGetDistinctMagazineNamesAndCountForSearchedTerm:
    def test_type_of_get_distinct_magazine_names_and_count_for_searched_term(
        self, test_client
    ):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object with all details for
        # a searched term to be grouped and counted
        details_for_searched_term = get_details_for_searched_term(s_word)

        magazine_names_and_count = (
            get_distinct_magazine_names_and_count_for_searched_term(
                details_for_searched_term
            )
        )

        assert isinstance(magazine_names_and_count, flask_sqlalchemy.query.Query)

    def test_get_distinct_magazine_names_and_count_for_searched_term_gets_correct_data(
        self, test_client
    ):
        s_word = "Bucuresti"
        # get a flask_sqlalchemy.query.Query object with all details for
        # a searched term to be grouped and counted
        details_for_searched_term = get_details_for_searched_term(s_word)

        magazine_names_and_count = (
            get_distinct_magazine_names_and_count_for_searched_term(
                details_for_searched_term
            )
        )
        expected_result = [
            ("Albina (1866-1876)", 26),
            ("Amicul Şcoalei (1925-1935)", 186),
        ]

        assert list(magazine_names_and_count) == expected_result


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

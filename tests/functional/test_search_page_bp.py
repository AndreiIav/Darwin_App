import pytest

from application.search_page.logic import format_search_word

# Tests for /results/
def test_results_page_get(test_client):

    s_word = format_search_word("Victor Babes")
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Number of results displayed by magazine name" in response.data


def test_results_page_post(test_client):

    s_word = format_search_word("Victor Babes")
    response = test_client.post("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 405


results_page_pages = [1, 2, 23]


@pytest.mark.parametrize("pages", results_page_pages)
def test_results_page_pagination_existent_page(test_client, pages):

    s_word = format_search_word("Victor Babes")
    response = test_client.get(
        "/results/search",
        query_string={"search_box": s_word, "page": results_page_pages},
    )

    assert response.status_code == 200


def test_results_page_pagination_not_existent_page(test_client):

    s_word = format_search_word("Victor Babes")
    response = test_client.get(
        "/results/search", query_string={"search_box": s_word, "page": 24}
    )

    assert response.status_code == 404


def test_results_page_with_magazine_filter(test_client):

    s_word = "Victor+Babeș"
    magazine_filter = "Gazeta+de+Transilvania+(1838-1914)"

    response = test_client.get(
        "/results/search",
        query_string={"magazine_filter": magazine_filter, "search_box": s_word},
    )

    assert response.status_code == 200

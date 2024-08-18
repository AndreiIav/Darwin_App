import pytest


# Tests for /results/
def test_get_results_page(test_client):
    s_word = "Bucuresti"
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Number of results displayed by magazine name" in response.data


def test_post_results_page(test_client):
    s_word = "Victor+Babeș"
    response = test_client.post("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 405


page = [2, 10, 22]


@pytest.mark.parametrize("page", page)
def test_get_results_page_pagination_existent_page(test_client, page):
    s_word = "Bucuresti"
    response = test_client.get(
        "/results/search",
        query_string={"search_box": s_word, "page": page},
    )

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Number of results displayed by magazine name" in response.data


def test_get_results_page_pagination_not_existent_page(test_client):
    s_word = "Bucuresti"
    response = test_client.get(
        "/results/search", query_string={"search_box": s_word, "page": 23}
    )

    assert response.status_code == 404


def test_get_results_page_with_magazine_filter_first_page(test_client):
    s_word = "Bucuresti"
    magazine_filter = "Albina (1866-1876)"

    response = test_client.get(
        "/results/search",
        query_string={"magazine_filter": magazine_filter, "search_box": s_word},
    )

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Go back to all results" in response.data


page = [2, 3]


@pytest.mark.parametrize("page", page)
def test_get_results_page_with_magazine_filter_pagination_existent_page(
    test_client, page
):
    s_word = "Bucuresti"
    magazine_filter = "Albina (1866-1876)"

    response = test_client.get(
        "/results/search",
        query_string={
            "magazine_filter": magazine_filter,
            "search_box": s_word,
            "page": page,
        },
    )

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Go back to all results" in response.data


def test_get_results_page_with_magazine_filter_pagination_not_existent_page(
    test_client,
):
    s_word = "Bucuresti"
    magazine_filter = "Albina (1866-1876)"
    page = 4

    response = test_client.get(
        "/results/search",
        query_string={
            "magazine_filter": magazine_filter,
            "search_box": s_word,
            "page": page,
        },
    )

    assert response.status_code == 404


def test_get_results_page_with_accepted_special_characters(test_client):
    s_word = "-_.,„!?;:'"
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"No results were found for" in response.data


def test_get_results_page_with_unaccepted_special_characters(test_client):
    s_word = r"()&/\|~{}[]+=<>"

    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert (
        b"The search term can have at least 4 characters and at most 200."
        in response.data
    )

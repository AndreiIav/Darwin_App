import pytest

# Tests for /results/
def test_results_page_get(test_client, format_word):

    s_word = format_word("Victor Babes")
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Filter Results by Magazine Name" in response.data


def test_results_page_post(test_client, format_word):

    s_word = format_word("Victor Babes")
    response = test_client.post("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 405


pages = [1, 2, 23]


@pytest.mark.parametrize("pages", pages)
def test_results_page_pagination_existent_page(test_client, format_word, pages):

    s_word = format_word("Victor Babes")
    response = test_client.get(
        "/results/search", query_string={"search_box": s_word, "page": pages}
    )

    assert response.status_code == 200


def test_results_page_pagination_not_existent_page(test_client, format_word):

    s_word = format_word("Victor Babes")
    response = test_client.get(
        "/results/search", query_string={"search_box": s_word, "page": 24}
    )

    assert response.status_code == 404


def test_results_page_with_magazine_filter(test_client, format_word):

    pass

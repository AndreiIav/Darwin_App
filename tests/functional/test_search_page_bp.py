import pytest

# Tests for /results/
def test_results_page_get(test_client):

    s_word = "Victor+Babeș"
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"Go back to home page" in response.data
    assert b"Number of results displayed by magazine name" in response.data

def test_results_page_post(test_client):

    s_word = "Victor+Babeș"
    response = test_client.post("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 405

results_page_pages = [1, 2, 23]
@pytest.mark.parametrize("pages", results_page_pages)
def test_results_page_pagination_existent_page(test_client, pages):

    s_word = "Victor+Babeș"
    response = test_client.get(
        "/results/search",
        query_string={"search_box": s_word, "page": results_page_pages},
    )

    assert response.status_code == 200

def test_results_page_pagination_not_existent_page(test_client):

    s_word = "Victor+Babeș"
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

def test_results_page_with_magazine_filter_pagination(test_client):

    s_word = "Victor+Babeș"
    magazine_filter = "Gazeta+de+Transilvania+(1838-1914)"
    page = 2

    response = test_client.get(
        "/results/search",
        query_string={"magazine_filter": magazine_filter, "search_box": s_word, "page": page},
    )

    assert response.status_code == 200

def test_results_page_with_accepted_special_characters(test_client):

    s_word = "-_.,„!?;:'"
    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"No results were found for" in response.data

def test_results_page_with_unaccepted_special_characters(test_client):

    s_word = "()&/\|~{}[]+=<>"

    response = test_client.get("/results/search", query_string={"search_box": s_word})

    assert response.status_code == 200
    assert b"The search term can have at least 4 characters and at most 200." in response.data
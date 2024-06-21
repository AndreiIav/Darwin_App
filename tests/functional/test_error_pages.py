import pytest


def test_404_response_in_magazine_details_page_because_magazine_id_is_not_found(
    test_client,
):
    response = test_client.get("/magazine_details", query_string={"magazine_id": 0})

    assert response.status_code == 404


def test_404_response_in_magazine_details_page_because_ValueError_is_raised(
    test_client,
):
    response = test_client.get("/magazine_details", query_string={"magazine_id": "a"})

    assert response.status_code == 404


def test_404_response_in_magazine_details_page_because_TypeError_is_raised(test_client):
    response = test_client.get("/magazine_details", query_string={"magazine_id": []})

    assert response.status_code == 404


@pytest.mark.parametrize("incorrect_input", ["a", "abc", "a" * 201])
def test_no_results_found_in_search_page_due_to_incorrect_lenghth_of_input(
    test_client, incorrect_input
):
    response = test_client.get(
        "/results/search", query_string={"search_box": incorrect_input}
    )

    assert response.status_code == 200
    assert b"No results found." in response.data
    assert (
        b"The search term can have at least 4 characters and at most 200."
        in response.data
    )


def test_no_results_found_in_search_page_due_to_not_found_term(test_client):
    term = "supercalifragilistic"
    response = test_client.get("/results/search", query_string={"search_box": term})

    assert response.status_code == 200
    assert b"No results found." in response.data
    assert b"No results were found for" in response.data
    assert term.encode() in response.data

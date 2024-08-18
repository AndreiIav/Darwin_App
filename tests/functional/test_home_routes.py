import json

import pytest


# Tests for "/" page
def test_get_home_page(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert b"Please introduce a search term in the box" in response.data


# Tests for "/magazine_details" page
def test_get_magazine_details_page(test_client):
    response = test_client.get("/magazine_details", query_string={"magazine_id": "4"})

    assert response.status_code == 200
    assert b"Albina (1866-1876)" in response.data


invalid_magazine_id_input = ["a", True, 1.23, None, "33"]


@pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
def test_get_magazine_details_page_with_invalid_magazine_id_parameter(
    test_client, invalid_magazine_id
):
    response = test_client.get(
        "/megazine_details", query_string={"magazine_id": invalid_magazine_id}
    )

    assert response.status_code == 404


# Tests for "/contact" page
def test_get_contact_page(test_client):
    response = test_client.get("/contact")

    assert response.status_code == 200
    assert b"Contact" in response.data


# Tests for "/about" page
def test_get_about_page(test_client):
    response = test_client.get("/about")

    assert response.status_code == 200
    assert b"About" in response.data


# Tests for "/log_magazine_click"
def test_get_log_magazine_click(test_client):
    response = test_client.get("/log_magazine_click")

    assert response.status_code == 405


def test_post_log_magazine_click(test_client):
    data = {"link": "test_link"}

    response = test_client.post(
        "/log_magazine_click",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200

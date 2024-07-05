import json

import pytest


# Tests for "/" page
def test_home_page_get(test_client):
    response = test_client.get("/")

    assert response.status_code == 200


# Tests for "/magazine_details" page
def test_magazine_details_page_get(test_client):
    response = test_client.get("/magazine_details", query_string={"magazine_id": "4"})

    assert response.status_code == 200
    assert b"Albina (1866-1876)" in response.data


invalid_magazine_id_input = ["a", True, 1.23, None, "33"]


@pytest.mark.parametrize("invalid_magazine_id", invalid_magazine_id_input)
def test_magazine_details_page_get_with_invalid_magazine_id_parameter(
    test_client, invalid_magazine_id
):
    response = test_client.get(
        "/megazine_details", query_string={"magazine_id": invalid_magazine_id}
    )

    assert response.status_code == 404


# Tests for "/contact" page
def test_contact_page_get(test_client):
    response = test_client.get("/contact")

    assert response.status_code == 200


# Tests for "/about" page
def test_about_page_get(test_client):
    response = test_client.get("/about")

    assert response.status_code == 200


# Tests for "/log_magazine_click"
def test_log_magazine_click_get(test_client):
    response = test_client.get("/log_magazine_click")

    assert response.status_code == 405


def test_log_magazine_click_post(test_client):
    data = {"link": "test_link"}

    response = test_client.post(
        "/log_magazine_click",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200

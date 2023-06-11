# Tests for "/" page
def test_home_page_get(test_client):
    response = test_client.get("/")

    assert response.status_code == 200


def test_home_page_post(test_client):
    response = test_client.post("/")

    assert response.status_code == 405


# Tests for "/magazine_details" page
def test_magazine_details_page_get(test_client):
    response = test_client.get("/magazine_details", query_string={"magazine_id": "4"})

    assert response.status_code == 200
    assert b"Albina (1866-1876)" in response.data

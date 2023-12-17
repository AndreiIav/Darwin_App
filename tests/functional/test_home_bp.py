
# Tests for "/" page
def test_home_page_get(test_client):
    response = test_client.get("/")

    assert response.status_code == 200

# Tests for "/magazine_details" page
def test_magazine_details_page_get(test_client):
    response = test_client.get("/magazine_details", query_string={"magazine_id": "4"})

    assert response.status_code == 200
    assert b"Albina (1866-1876)" in response.data

# Tests for "/contact" page
def test_contact_page_get(test_client):
    response = test_client.get("/contact")

    assert response.status_code == 200

# Tests for "/about" page
def test_about_page_get(test_client):
    response = test_client.get("/about")

    assert response.status_code == 200

import json


# Tests for "/log/log_magazine_click"
def test_get_log_magazine_link_click(test_client):
    response = test_client.get("/log/log_click_magazine_link")

    assert response.status_code == 405


def test_post_log_magazine_link_click(test_client):
    data = {"link": "test_link"}

    response = test_client.post(
        "/log/log_click_magazine_link",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200

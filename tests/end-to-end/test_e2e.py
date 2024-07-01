import re
from playwright.sync_api import expect


class TestHomePageE2E:

    def test_home_page_is_accessed(self, page, start_app_server):

        go_to_page = start_app_server
        page.goto(go_to_page)

        expect(page).to_have_title("BCU-Search")

    def test_home_locate_important_elements(self, page, start_app_server):

        go_to_page = start_app_server
        page.goto(go_to_page)

        expect(page.get_by_test_id("navigation_bar")).to_be_visible()
        expect(page.get_by_test_id("introduce_search_term_info")).to_be_visible()
        expect(page.get_by_placeholder("you can enter between 4 and")).to_be_visible()
        expect(page.get_by_placeholder("you can enter between 4 and")).to_be_empty()
        expect(page.get_by_test_id("search_button")).to_be_visible()

        expect(page.get_by_test_id("available_magazines_info")).to_be_visible()
        expect(page.get_by_test_id("available_magazines")).to_be_visible()

    def test_home_clicking_on_magazine_name_opens_magazine_details(
        self, page, start_app_server
    ):

        start_page = start_app_server

        page.goto(start_page)
        with page.expect_popup() as new_page:
            page.get_by_role("button", name="Albina (1866-1876)").click()
        magazine_details_page = new_page.value

        expect(magazine_details_page).to_have_title("Albina (1866-1876)-BCU-Search")

    def test_home_searching_with_valid_term_opens_search_page(
        self, page, start_app_server
    ):

        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        expect(page).to_have_title("Search Results-BCU-Search")

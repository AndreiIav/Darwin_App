import re
from playwright.sync_api import expect


class TestHomePage:

    def test_home_page_is_accessed(self, page, start_app_server):

        go_to_page = start_app_server
        page.goto(go_to_page)

        expect(page).to_have_title(re.compile("BCU-Search"))

    def test_home_locate_all_elements(self, page, start_app_server):

        go_to_page = start_app_server
        page.goto(go_to_page)

        expect(page.get_by_text("Home About Contact")).to_be_visible()

        expect(
            page.get_by_text("Please introduce a search term in the box")
        ).to_be_visible()

        expect(page.get_by_placeholder("you can enter between 4 and")).to_be_visible()
        expect(page.get_by_placeholder("you can enter between 4 and")).to_be_empty()

        expect(page.get_by_role("button", name="Search")).to_be_visible()

        expect(
            page.get_by_role(
                "heading",
                name="The submited term will be searched in the following magazines",
            )
        ).to_be_visible()

        expect(
            page.locator("form").filter(has_text="Albina (1866-1876)")
        ).to_be_visible()
        expect(
            page.locator("form").filter(has_text="Amicul Şcoalei (1925-1935)")
        ).to_be_visible()

    def test_home_clicking_on_magazine_name_opens_magazine_details(
        self, page, start_app_server
    ):

        start_page = start_app_server

        page.goto(start_page)
        with page.expect_popup() as new_page:
            page.get_by_role("button", name="Albina (1866-1876)").click()
        magazine_details_page = new_page.value

        expect(magazine_details_page).to_have_title(" Albina (1866-1876)-BCU-Search ")

    def test_home_searching_with_valid_term_opens_search_page(
        self, page, start_app_server
    ):

        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        expect(page).to_have_title(" Search Results-BCU-Search ")

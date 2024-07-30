from playwright.sync_api import expect


class TestHomePageE2E:
    def test_home_page_is_accessed(self, page, start_app_server):
        go_to_page = start_app_server
        page.goto(go_to_page)

        expect(page).to_have_title("Home")

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

        expect(page).to_have_title("Search Results")


class TestSearchPageE2E:
    def test_search_page_locate_important_elements(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        expect(page.get_by_test_id("navigation_bar")).to_be_visible()
        expect(page.get_by_test_id("go_back_home")).to_be_visible()
        expect(page.get_by_test_id("count_results")).to_be_visible()
        expect(
            page.get_by_test_id("display_count_results_per_magazine")
        ).to_be_visible()
        expect(page.get_by_test_id("displayed_results")).to_be_visible()
        expect(page.get_by_test_id("pagination")).to_be_visible()
        # check that the count results are not collapsed/visible
        expect(page.get_by_test_id("collapsed_count_results")).not_to_have_class(
            "collapse show"
        )

    def test_go_back_to_home_page_button_opens_home_page(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        expect(page).to_have_title("Search Results")

        page.get_by_test_id("go_back_home").click()

        expect(page).to_have_title("Home")

    def test_display_count_results_per_magazine_button(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        # check that the count results are visible after clicking the button
        page.get_by_test_id("display_count_results_per_magazine").click()
        expect(page.get_by_test_id("collapsed_count_results")).to_have_class(
            "collapse show"
        )

        # check that the count results are not visible after clicking the
        # button once more
        page.get_by_test_id("display_count_results_per_magazine").click()
        expect(page.get_by_test_id("collapsed_count_results")).not_to_have_class(
            "collapse show"
        )

    def test_add_magazine_filter(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")
        page.get_by_test_id("display_count_results_per_magazine").click()
        page.get_by_role("button", name="Albina (1866-1876) (26").click()

        expect(page.get_by_test_id("go_back_to_all_results")).to_be_visible()
        expect(
            page.get_by_test_id("count_results_with_magazine_filter")
        ).to_be_visible()

    def test_go_back_to_all_results_button(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")
        page.get_by_test_id("display_count_results_per_magazine").click()
        page.get_by_role("button", name="Albina (1866-1876) (26").click()
        page.get_by_test_id("go_back_to_all_results").click()

        # the go_back_to_all_results and count_results_with_magazine_filter
        # elements should not be visible anymore
        expect(page.get_by_test_id("go_back_to_all_results")).not_to_be_visible()
        expect(
            page.get_by_test_id("count_results_with_magazine_filter")
        ).not_to_be_visible()

    def test_displayed_results_have_correct_elements(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        # with the default settings there should be 10 results on the page
        expect(page.get_by_test_id("result")).to_have_count(10)
        expect(page.get_by_test_id("name")).to_have_count(10)
        expect(page.get_by_test_id("year")).to_have_count(10)
        expect(page.get_by_test_id("magazine_number")).to_have_count(10)
        expect(page.get_by_test_id("magazine_page")).to_have_count(10)
        expect(page.get_by_test_id("magazine_number_link")).to_have_count(10)
        expect(page.get_by_test_id("preview_content")).to_have_count(10)

    def test_magazine_link_will_open_a_different_tab(self, page, start_app_server):
        start_page = start_app_server

        page.goto(start_page)
        page.get_by_placeholder("you can enter between 4 and").click()
        page.get_by_placeholder("you can enter between 4 and").fill("bucuresti")
        page.get_by_placeholder("you can enter between 4 and").press("Enter")

        expect(
            page.get_by_test_id("displayed_results")
            .locator("div")
            .filter(
                has_text="Albina (1866-1876) ANUL 1866 Nr.1 Page 2 Open Magazine [...] inimicii.—"
            )
            .get_by_test_id("link")
        ).to_have_attribute("target", "_blank")

    class TestNavigationBarE2E:
        def test_navigation_bar_has_correct_links(self, page, start_app_server):
            start_page = start_app_server

            page.goto(start_page)

            expect(page.get_by_test_id("navigation_bar")).to_be_visible()
            expect(page.get_by_role("link", name="Home")).to_be_visible()
            expect(page.get_by_role("link", name="About")).to_be_visible()
            expect(page.get_by_role("link", name="Contact")).to_be_visible()

        def test_navigation_bar_links_work(self, page, start_app_server):
            start_page = start_app_server

            page.goto(start_page)

            page.get_by_role("link", name="About").click()
            expect(page).to_have_title("About")

            page.get_by_role("link", name="Contact").click()
            expect(page).to_have_title("Contact")

            page.get_by_role("link", name="Home").click()
            expect(page).to_have_title("Home")

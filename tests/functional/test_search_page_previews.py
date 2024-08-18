from application.search_page.previews import get_previews_for_page_id


# Tests for get_previews_for_page_id
class TestGetPreviewsForPageId:
    def test_get_previews_for_page_id_length_of_response_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert len(res) == 1

    def test_get_previews_for_page_id_response_type_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        s_word, paginated_details_for_searched_term = (
            set_up_data_for_previews_for_page_id[0],
            set_up_data_for_previews_for_page_id[2],
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=100
        )

        assert isinstance(res, list)
        assert isinstance(res[0][0], int)
        assert isinstance(res[0][1], str)

    def test_get_previews_for_page_id_response_content_is_correct(
        self, test_client, set_up_data_for_previews_for_page_id
    ):
        (
            s_word,
            page_id,
            paginated_details_for_searched_term,
        ) = set_up_data_for_previews_for_page_id

        expected_page_id = page_id
        expected_preview_text = (
            "<b><i>[...]</i></b> Cojocariu proprietariu. D. <mark>Andrei Mocioni</mark>"
            + " „ Paulu Vasiciu. oons <b><i>[...]</i></b>"
        )

        res = get_previews_for_page_id(
            paginated_details_for_searched_term, s_word=s_word, preview_length=20
        )

        print(res[0][1])

        assert res[0][0] == expected_page_id
        assert res[0][1] == expected_preview_text

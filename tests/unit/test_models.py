from application.models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContent,
    MagazineNumberContentFTS,
    MagazineDetails,
)


class TestModels:
    def test_Magazines(self):
        magazine = Magazines(id=1, name="testName", magazine_link="testMagazineLink")

        assert magazine.id == 1
        assert magazine.name == "testName"
        assert magazine.magazine_link == "testMagazineLink"
        assert (
            repr(magazine)
            == "Magazines(id=1,name=testName,magazine_link=testMagazineLink)"
        )

    def test_MagazineYear(self):
        magazine_year = MagazineYear(
            id=1,
            magazine_id=1,
            year="testYear",
            magazine_year_link="testMagazineYearLink",
        )

        assert magazine_year.id == 1
        assert magazine_year.magazine_id == 1
        assert magazine_year.year == "testYear"
        assert magazine_year.magazine_year_link == "testMagazineYearLink"
        assert (
            repr(magazine_year)
            == "MagazineYear(id=1,magazine_id=1,year=testYear,magazine_year_link=testMagazineYearLink)"
        )

    def test_MagazineNumber(self):
        magazine_number = MagazineNumber(
            id=1,
            magazine_year_id=2,
            magazine_number="testMagazineNumber",
            magazine_number_link="testMagazineNumberLink",
        )

        assert magazine_number.id == 1
        assert magazine_number.magazine_year_id == 2
        assert magazine_number.magazine_number == "testMagazineNumber"
        assert magazine_number.magazine_number_link == "testMagazineNumberLink"
        assert (
            repr(magazine_number)
            == "MagazineNumber(id=1,magazine_year_id=2,magazine_number=testMagazineNumber,magazine_number_link=testMagazineNumberLink)"
        )

    def test_MagazineNumberContent(self):
        magazine_number_content = MagazineNumberContent(
            id=1,
            magazine_number_id=2,
            magazine_content="testContent",
            magazine_page="3",
        )

        assert magazine_number_content.id == 1
        assert magazine_number_content.magazine_number_id == 2
        assert magazine_number_content.magazine_content == "testContent"
        assert magazine_number_content.magazine_page == "3"
        assert (
            repr(magazine_number_content)
            == "MagazineNumberContent(id=1,magazine_number_id=2,magazine_content=testContent,magazine_page=3)"
        )

    def test_MagazineNumberContentFTS(self):
        magazine_number_content_fts = MagazineNumberContentFTS(
            rowid=1, magazine_content="testMagazineContent"
        )

        assert magazine_number_content_fts.rowid == 1
        assert magazine_number_content_fts.magazine_content == "testMagazineContent"
        assert (
            repr(magazine_number_content_fts)
            == "MagazineNumberContentFTS(rowid=1,magazine_content=testMagazineContent)"
        )

    def test_MagazineDetails(self):
        magazine_details = MagazineDetails(
            id=1,
            magazine_id=1,
            year="Anul 1899",
            distinct_magazine_numbers_count=10,
            distinct_pages_count=100,
        )

        assert magazine_details.id == 1
        assert magazine_details.magazine_id == 1
        assert magazine_details.year == "Anul 1899"
        assert magazine_details.distinct_magazine_numbers_count == 10
        assert magazine_details.distinct_pages_count == 100
        assert (
            repr(magazine_details)
            == "MagazineDetails(id=1,magazine_id=1,year=Anul 1899,distinct_magazine_numbers_count=10,distinct_pages_count=100)"
        )

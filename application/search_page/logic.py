from ..models import Magazines, MagazineYear, MagazineNumber, MagazineNumberContent, db


def get_json_details_for_searched_term(s_word, page):

    q = (
        db.session.query(
            Magazines.name,
            MagazineYear.year,
            MagazineNumber.magazine_number,
            MagazineNumberContent.magazine_page,
            MagazineNumber.magazine_number_link,
        )
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContent,
            MagazineNumber.id == MagazineNumberContent.magazine_number_id,
        )
        .filter(MagazineNumberContent.magazine_content.like("%" + s_word + "%"))
    )

    response = q.paginate(page=page, per_page=10)

    return response

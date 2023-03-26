from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContent,
    MagazineNumberContentFTS,
    db,
)
from sqlalchemy import func


def get_details_for_searched_term(s_word, page, magazine_filter):
    """
    A function that returns a sqlAlchemy pagination object containing the Magazines.name,
    MagazineYear.year, MagazineNumber.magazine_number, MagazineNumberContent.magazine_page,
    MagazineNumber.magazine_number_link
    """

    if magazine_filter is None:

        all_details_for_searched_term = (
            db.session.query(
                Magazines.name,
                MagazineYear.year,
                MagazineNumber.magazine_number,
                MagazineNumberContentFTS.magazine_page,
                MagazineNumber.magazine_number_link,
            )
            .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
            .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
            .join(
                MagazineNumberContentFTS,
                MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
            )
            .filter(MagazineNumberContentFTS.magazine_content.match(f"{s_word}*"))
        )

    else:

        all_details_for_searched_term = (
            db.session.query(
                Magazines.name,
                MagazineYear.year,
                MagazineNumber.magazine_number,
                MagazineNumberContentFTS.magazine_page,
                MagazineNumber.magazine_number_link,
            )
            .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
            .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
            .join(
                MagazineNumberContentFTS,
                MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
            )
            .filter(MagazineNumberContentFTS.magazine_content.match(f"{s_word}*"))
        ).filter(Magazines.name == magazine_filter)

    response = all_details_for_searched_term.paginate(page=page, per_page=10)
    return response


def get_distinct_magazine_names_and_count_for_searched_term(s_word):

    distinct_magazine_names_and_count_for_searched_term = (
        db.session.query(Magazines.name, func.count(Magazines.name))
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContentFTS,
            MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
        )
        .filter(MagazineNumberContentFTS.magazine_content.match(f"{s_word}*"))
        .group_by(Magazines.name)
    )

    return distinct_magazine_names_and_count_for_searched_term

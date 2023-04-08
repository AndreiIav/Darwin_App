from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContentFTS,
    db,
)
from sqlalchemy import func


def get_details_for_searched_term(formated_s_word, page, magazine_filter):
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
                MagazineNumberContentFTS.rowid,
            )
            .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
            .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
            .join(
                MagazineNumberContentFTS,
                MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
            )
            .filter(
                MagazineNumberContentFTS.magazine_content.match(f'"{formated_s_word}"*')
            )
        )

    else:

        all_details_for_searched_term = (
            db.session.query(
                Magazines.name,
                MagazineYear.year,
                MagazineNumber.magazine_number,
                MagazineNumberContentFTS.magazine_page,
                MagazineNumber.magazine_number_link,
                MagazineNumberContentFTS.rowid,
            )
            .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
            .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
            .join(
                MagazineNumberContentFTS,
                MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
            )
            .filter(
                MagazineNumberContentFTS.magazine_content.match(f'"{formated_s_word}"*')
            )
        ).filter(Magazines.name == magazine_filter)

    response = all_details_for_searched_term.paginate(page=page, per_page=10)
    return response


def get_distinct_magazine_names_and_count_for_searched_term(formated_s_word):

    distinct_magazine_names_and_count_for_searched_term = (
        db.session.query(Magazines.name, func.count(Magazines.name))
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContentFTS,
            MagazineNumber.id == MagazineNumberContentFTS.magazine_number_id,
        )
        .filter(
            MagazineNumberContentFTS.magazine_content.match(f'"{formated_s_word}"*')
        )
        .group_by(Magazines.name)
    )

    return distinct_magazine_names_and_count_for_searched_term


def format_search_word(s_word):

    s_word_list = s_word.split()

    if len(s_word_list) == 1:
        formated_s_word = s_word
    else:
        formated_s_word = "+".join(s_word_list)

    return formated_s_word


def get_magazine_content_details(page_id):

    magazine_content_details = db.session.query(
        MagazineNumberContentFTS.magazine_content
    ).filter(MagazineNumberContentFTS.rowid == page_id)

    return magazine_content_details[0][0]

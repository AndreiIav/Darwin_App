from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContent,
    db,
)
from sqlalchemy import func


def get_existent_magazines():

    res = db.session.query(Magazines.name, Magazines.id)
    return res


def get_magazine_name(magazine_id):

    magazine_name = db.session.get(Magazines, magazine_id)
    return magazine_name.name


def get_magazine_details(magazine_id):

    magazine_details = (
        db.session.query(
            MagazineYear.year,
            func.count(func.distinct(MagazineNumber.id)),
            func.count(func.distinct(MagazineNumberContent.id)),
        )
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContent,
            MagazineNumber.id == MagazineNumberContent.magazine_number_id,
        )
        .filter(MagazineYear.magazine_id == magazine_id)
        .group_by(MagazineYear.id)
    )

    return magazine_details

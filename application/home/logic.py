from ..models import Magazines, MagazineYear, MagazineNumber, db
from sqlalchemy import func


def get_existent_magazines():

    res = db.session.query(Magazines.name, Magazines.id)

    return res


def get_magazine_details(magazine_id):

    magazine_details = (
        db.session.query(
            Magazines.name,
            MagazineYear.year,
            func.count(MagazineNumber.magazine_number),
        )
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .group_by(Magazines.id, MagazineYear.id)
        .filter(Magazines.id == magazine_id)
    )

    return magazine_details

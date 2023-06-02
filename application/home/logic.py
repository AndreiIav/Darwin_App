from ..models import (
    Magazines,
    MagazineYear,
    MagazineNumber,
    MagazineNumberContent,
    db,
)
from sqlalchemy import func


def get_existent_magazines():
    """
    This function returns a SQLAlchemy Query object that retrieves the names and ids of magazines
    from the Magazines table.
    The Query object can be iterated to access the results.
    """

    existent_magazines = db.session.query(Magazines.name, Magazines.id)
    return existent_magazines


def get_magazine_name(magazine_id=0):
    """
    "This function retrieves the name of a magazine from the Magazines table using the provided magazine_id.
    If a magazine with the specified id exists, it returns the corresponding magazine name as a string.
    If the magazine_id is not found or is of an invalid data type, it returns None."
    """

    try:
        magazine_id = int(magazine_id)
    except ValueError:
        return
    except TypeError:
        return

    magazine_name = db.session.get(Magazines, magazine_id)

    if magazine_name is not None:
        return magazine_name.name

    return


def get_magazine_details(magazine_id=0):
    """
    This function returns a SQLAlchemy Query object that retrieves MagazineYear instances for a given magazine_id.
    Each MagazineYear instance includes the distinct count of magazine numbers and pages associated with that year.
    The Query object can be iterated to access the results.
    If the magazine_id is not found or is of an invalid data type, the Query object will be empty.
    """

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

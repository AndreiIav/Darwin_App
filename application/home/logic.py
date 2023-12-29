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
    Retrieve the names and ids of magazines from the Magazines table.

    Returns:
        existent_magazines (flask_sqlalchemy.query.Query): A Query object containing
        the retrieved names and ids.

    The Query object can be iterated to access the results.
    """

    existent_magazines = db.session.query(Magazines.name, Magazines.id).order_by(Magazines.name)
    return existent_magazines


def get_magazine_name(magazine_id=0):
    """
    Retrieve the name of a magazine from the Magazines table based on the provided magazine_id.

    Args:
        magazine_id (int, optional): The ID of the magazine to retrieve the name for. Defaults to 0.

    Returns:
        magazine_name.name (str) or None: The name of the magazine if found, or None if the
        magazine_id is not found or is of an invalid data type.
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
    Retrieve MagazineYear instances for a given magazine_id.

    Args:
        magazine_id (int, optional): The ID of the magazine to retrieve details for. Defaults to 0.

    Returns:
        magazine_details (flask_sqlalchemy.query.Query): A Query object containing MagazineYear
        instances with associated counts.

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
        .order_by(MagazineYear.year)
    )

    return magazine_details

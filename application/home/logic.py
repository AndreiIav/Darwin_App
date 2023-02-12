from ..models import Magazines, db


def get_existent_magazines(page):

    res = db.paginate(db.select(Magazines), page=page, per_page=20)

    return res

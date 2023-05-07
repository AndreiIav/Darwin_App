from ..models import Magazines, db


def get_existent_magazines():

    res = db.session.query(Magazines.name)

    return res

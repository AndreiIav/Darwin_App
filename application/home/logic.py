from ..models import Magazines, db


def get_existent_magazines():

    existent_magazines = []

    res = db.session.execute(db.select(Magazines.name))

    for result in res:
        existent_magazines.append(result[0])

    return existent_magazines

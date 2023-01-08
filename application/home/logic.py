from application.db import get_db


def get_existent_magazines():

    existent_magazines = []

    db = get_db()
    res = db.execute(
        "SELECT name FROM magazines",
    ).fetchall()

    for result in res:
        existent_magazines.append(result[0])

    return existent_magazines

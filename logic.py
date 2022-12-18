import sqlite3
from db import get_db


def get_count(s_word):

    db = get_db()
    res = db.execute(
        "SELECT COUNT(*) FROM magazine_number_content WHERE magazine_content LIKE :word",
        {"word": "%" + s_word + "%"},
    ).fetchone()[0]

    return res

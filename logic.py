import sqlite3


def get_count(s_word):

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM magazine_number_content WHERE magazine_content LIKE :word",
        {"word": "%" + s_word + "%"},
    )
    res = c.fetchone()[0]
    conn.close()
    return res

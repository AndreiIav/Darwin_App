import sqlite3


# def get_searched_term_from_form():
#     return request.form.get("search_term", "default")


def get_count(s_word):
    # s_word = request.form.get("search_term", "default")

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM magazine_number_content WHERE magazine_content LIKE :word",
        {"word": "%" + s_word + "%"},
    )
    res = c.fetchone()[0]
    conn.close()
    return res

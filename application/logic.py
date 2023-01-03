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


def get_json_details_for_searched_term(s_word):

    db = get_db()
    all_res = db.execute(
        """
          SELECT DISTINCT m.name, ma.year, mn.magazine_number, mnc.magazine_page, mn.magazine_number_link
          FROM magazines m
          INNER JOIN magazine_year ma ON m.id = ma.magazine_id
          INNER JOIN magazine_number mn ON ma.id = mn.magazine_year_id
          INNER JOIN magazine_number_content mnc ON mn.id = mnc.magazine_number_id
          WHERE mnc.magazine_content LIKE :word
          ORDER BY m.name
        """,
        {"word": "%" + s_word + "%"},
    ).fetchall()

    response = []
    for res in all_res:

        partial_values = {}
        partial_values["magazine_name"] = res[0]
        partial_values["magazine_year"] = res[1]
        partial_values["magazine_number"] = res[2]
        partial_values["page"] = res[3]
        partial_values["link"] = res[4]

        response.append(partial_values)

    return response

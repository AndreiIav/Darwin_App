from ..models import Magazines, MagazineYear, MagazineNumber, MagazineNumberContent, db


def get_json_details_for_searched_term(s_word, page):

    # all_res = db.session.execute(
    #     db.select(
    #         Magazines.name,
    #         MagazineYear.year,
    #         MagazineNumber.magazine_number,
    #         MagazineNumberContent.magazine_page,
    #         MagazineNumber.magazine_number_link,
    #     )
    #     .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
    #     .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
    #     .join(
    #         MagazineNumberContent,
    #         MagazineNumber.id == MagazineNumberContent.magazine_number_id,
    #     )
    #     .where(MagazineNumberContent.magazine_content.like("%" + s_word + "%"))
    # ).all()

    # response = []
    # for res in all_res:

    #     partial_values = {}
    #     partial_values["magazine_name"] = res[0]
    #     partial_values["magazine_year"] = res[1]
    #     partial_values["magazine_number"] = res[2]
    #     partial_values["page"] = res[3]
    #     partial_values["link"] = res[4]

    #     response.append(partial_values)

    q = (
        db.session.query(
            Magazines.name,
            MagazineYear.year,
            MagazineNumber.magazine_number,
            MagazineNumberContent.magazine_page,
            MagazineNumber.magazine_number_link,
        )
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContent,
            MagazineNumber.id == MagazineNumberContent.magazine_number_id,
        )
        .filter(MagazineNumberContent.magazine_content.like("%" + s_word + "%"))
    )

    response = q.paginate(page=page, per_page=10)

    return response

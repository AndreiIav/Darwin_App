from sqlalchemy import func

from application.models import (
    MagazineNumber,
    MagazineNumberContent,
    MagazineNumberContentFTS,
    Magazines,
    MagazineYear,
    db,
)


def get_details_for_searched_term(formatted_s_word):
    """
    Retrieve specific columns from multiple tables based on a provided search
    term.

    Args:
        formatted_s_word (str): The search term used for retrieval.

    Returns:
        all_details_for_searched_term (flask_sqlalchemy.query.Query): A Query
        object containing the retrieved results.

    This function returns a SQLAlchemy Query object that retrieves specific
    columns (Magazines.name, MagazineYear.year, MagazineNumber.magazine_number,
    MagazineNumberContent.magazine_page, MagazineNumber.magazine_number_link,
    and MagazineNumberContent.id) from multiple tables based on a provided
    search term.
    The search is performed on an FTS5 table, which enables fast text search
    capabilities.
    The Query object can be iterated to access the results.
    """

    expression_to_search = '"' + formatted_s_word + '"' + "*"

    all_details_for_searched_term = (
        db.session.query(
            Magazines.name,
            MagazineYear.year,
            MagazineNumber.magazine_number,
            MagazineNumberContent.magazine_page,
            MagazineNumber.magazine_number_link,
            MagazineNumberContent.id,
        )
        .join(MagazineYear, Magazines.id == MagazineYear.magazine_id)
        .join(MagazineNumber, MagazineYear.id == MagazineNumber.magazine_year_id)
        .join(
            MagazineNumberContent,
            MagazineNumber.id == MagazineNumberContent.magazine_number_id,
        )
        .join(
            MagazineNumberContentFTS,
            MagazineNumberContent.id == MagazineNumberContentFTS.rowid,
        )
        .filter(MagazineNumberContentFTS.magazine_content.match(expression_to_search))
        .order_by(
            Magazines.name,
            MagazineYear.year,
            MagazineNumber.magazine_number,
            MagazineNumberContent.magazine_page,
        )
    )

    return all_details_for_searched_term


def get_details_for_searched_term_for_specific_magazine(
    details_for_searched_term, magazine_filter
):
    """
    Filter a SQLAlchemy Query object based on a provided filter term.

    Args:
        details_for_searched_term (flask_sqlalchemy.query.Query): The Query
        object returned by the get_details_for_searched_term function.
        magazine_filter (str): The filter term representing Magazines.name.

    Returns:
        details_for_specific_magazine (flask_sqlalchemy.query.Query): A new
        Query object containing the filtered results.
    """

    details_for_specific_magazine = details_for_searched_term.filter(
        Magazines.name == magazine_filter
    )

    return details_for_specific_magazine


def paginate_results(details_for_searched_term, page, per_page, error_out):
    """
    Generate a SQLAlchemy Pagination object for the provided Query.

    Args:
        details_for_searched_term (flask_sqlalchemy.query.Query): The SQLAlchemy
        Query object to paginate.
        page (int): The page number to retrieve.
        per_page (int): The number of results to be displayed on a page.
        error_out (bool): The error flag for the error_out argument for the
        pagination object.

    Returns:
        flask_sqlalchemy.pagination.QueryPagination: A Pagination object
        representing the subset of query results for the requested page.
    """
    return details_for_searched_term.paginate(
        page=page, per_page=per_page, error_out=error_out
    )


def get_distinct_magazine_names_and_count_for_searched_term(details_for_searched_term):
    """
    Retrieve distinct magazine names and search term counts.

    Args:
        details_for_searched_term (flask_sqlalchemy.query.Query): A Query object
        containing all search results for a specific term.

    Returns:
        distinct_magazine_names_and_count_for_searched_term
        (flask_sqlalchemy.query.Query): A Query object containing tuples of
        magazine names and search term counts.

    The Query object can be iterated to access the magazine names and their
    respective search term counts.
    """

    subq = details_for_searched_term.subquery()
    distinct_magazine_names_and_count_for_searched_term = (
        db.session.query(Magazines.name, func.count(Magazines.name))
        .join(subq, Magazines.name == subq.c.name)
        .group_by(Magazines.id)
        .order_by(Magazines.name)
    )

    return distinct_magazine_names_and_count_for_searched_term

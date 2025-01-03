import csv
import sqlite3

import click


def create_database(database_path):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    # Create database and tables.
    with conn:
        c.executescript(
            """
            CREATE TABLE magazines(
            id integer PRIMARY KEY ,
            name text,
            magazine_link text);

            CREATE TABLE magazine_year(
            id integer PRIMARY KEY,
            magazine_id integer,
            year text,
            magazine_year_link text,
            FOREIGN KEY(magazine_id) REFERENCES magazines(id));

            CREATE TABLE magazine_number(
            id integer PRIMARY KEY,
            magazine_year_id integer,
            magazine_number text,
            magazine_number_link text,
            FOREIGN KEY(magazine_year_id) REFERENCES magazine_year(id));

            CREATE TABLE magazine_number_content(
            id integer PRIMARY KEY,
            magazine_number_id integer,
            magazine_content text,
            magazine_page id,
            FOREIGN KEY(magazine_number_id) REFERENCES magazine_number(id));
            """
        )


def write_data_to_database(files_path, database_path, files_to_tables):
    for file, table in files_to_tables:
        file_path = files_path / file

        try:
            data = get_data_from_csv_file(file_path)
        except FileNotFoundError:
            raise click.FileError(
                file_path,
                hint=f"The {file} file needed to create the"
                " database was not found.\n"
                "Check the csv files and try again.\n"
                "If a database file was already created use"
                " 'flask database remove <name_of_database>'"
                " command to delete it.",
            )

        write_to_database(database_path, table, data)


def get_data_from_csv_file(file_path):
    data = []

    with open(file_path, encoding="UTF-8-SIG") as f:
        csv_reader = csv.reader(f, delimiter=",")

        for row in csv_reader:
            data.append(tuple(row))

    return data


def write_to_database(database_path, table, data):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        if table == "magazines":
            c.executemany(
                "INSERT INTO magazines(id,name,magazine_link) VALUES(?,?,?)",
                data,
            )

        if table == "magazine_year":
            c.executemany(
                "INSERT INTO magazine_year(id,magazine_id,year,magazine_year_link) VALUES (?,?,?,?)",
                data,
            )

        if table == "magazine_number":
            c.executemany(
                "INSERT INTO magazine_number(id,magazine_year_id,magazine_number,magazine_number_link) VALUES (?,?,?,?)",
                data,
            )

        if table == "magazine_number_content":
            c.executemany(
                "INSERT INTO magazine_number_content(id,magazine_number_id,magazine_content,magazine_page) VALUES(?,?,?,?)",
                data,
            )


def create_magazine_details_table(database_path):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        c.executescript(
            """
            DROP TABLE IF EXISTS magazine_details
            ;

            CREATE TABLE IF NOT EXISTS magazine_details(
            id integer Primary Key,
            magazine_id integer,
            year text,
            distinct_magazine_numbers_count integer,
            distinct_pages_count integer,
            FOREIGN KEY(magazine_id) REFERENCES magazines(id)
            )
            ;

            INSERT INTO magazine_details(
                magazine_id,
                year,
                distinct_magazine_numbers_count,
                distinct_pages_count
                )
            SELECT
                m.id,
                my.year,
                COUNT(DISTINCT(mn.id)),
                COUNT(DISTINCT(mnc.id))
            FROM magazines m
            INNER JOIN magazine_year my ON m.id = my.magazine_id
            INNER JOIN magazine_number mn ON my.id = mn.magazine_year_id
            INNER JOIN magazine_number_content mnc ON mn.id = mnc.magazine_number_id
            GROUP BY my.id
            ORDER BY m.id, my.year
            ;
            """
        )


def create_fts_table(database_path, accepted_special_characters=""):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        # create the magazine_number_content_fts fts5 contentless table
        c.execute(
            f"""
            CREATE VIRTUAL TABLE magazine_number_content_fts USING fts5(
                magazine_content,
                content='',
                tokenize = "unicode61 remove_diacritics 2 tokenchars '{accepted_special_characters}'"
                )
            """
        )

        # populate the fts table
        c.execute(
            """
            INSERT INTO magazine_number_content_fts(rowid, magazine_content)
            SELECT id, magazine_content FROM magazine_number_content
            """
        )

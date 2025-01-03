"""cli_data_repository module

This module contains functions that create and populate a SQLite database and
functions that read data from CSV files.
"""

import csv
import sqlite3

import click


def create_database(database_path):
    """
    Create SQLite database file.

    Creates a SQLite database file with the following tables: magazines,
    magazine_year, magazine_number, magazine_number_content.

    Args:
        database_path (str): The path where the database file will be created.

    Returns:
        None
    """
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
    """
    Write data from multiple CSV files to specific tables in a database.

    This function reads data from a set of CSV files located in the given
    'files_path' directory and writes the data to corresponding tables in the
    specified database.
    This function uses two helper functions:
    - get_data_from_csv_file(file_path)
    - write_to_database(database_path, table, data)

    Args:
        files_path (Path): The directory containing the CSV files.
        database_path (Path): The file path to the database where the data will
        be written.
        files_to_tables (list of tuple): A list of tuples where each tuple maps
        a CSV file name (str) to a database table name (str).
        Example: [("data1.csv", "table1"), ("data2.csv", "table2")]

    Raises:
        click.FileError:  If a specified CSV file is not found in the
        'files_path' directory.
    """
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
    """
    Read data from a CSV file and return it as a list of tuples.

    This function opens a CSV file, reads its content, and parses each row into
    a tuple. The resulting list of tuples represents the data in the CSV file.

    Args:
        file_path (Path): The path to the CSV file to be read.

    Returns:
        list of tuple: A list where each element is a tuple representing a row
        in the CSV file.
    """
    data = []

    with open(file_path, encoding="UTF-8-SIG") as f:
        csv_reader = csv.reader(f, delimiter=",")

        for row in csv_reader:
            data.append(tuple(row))

    return data


def write_to_database(database_path, table, data):
    """
    Insert data into a specified table in a SQLite database.

    This function connects to a SQLite database and writes the provided data to
    the specified table. The supported tables are: magazines, magazine_year,
    magazine_number, magazine_number_content.

    Notes:
        - this function assumes that 'database_path' points to an existing SQLite
    database already created with create_database() function.

    Args:
        database_path (Path): The path to the SQLite database file.
        table (str): The name of the table to insert data into. Supported
        values are: 'magazines', 'magazine_year', 'magazine_number',
        'magazine_number_content'.
        data (list of tuple): The data to insert, where each tuple corresponds
        to a row.

    Returns:
        None

    """
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
    """
    Create and populate magazine_details table in a SQLite database.

    Notes:
        - this function assumes that 'database_path' points to an existing SQLite
    database already created with write_data_to_database() function.

    Args:
        database_path (Path): The path to the SQLite database file.
    Returns:
        None
    """
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
    """
    Create and populate magazine_number_content_fts table in a SQLite database.

    Creates and populates a contentless 'magazine_number_content_fts' table
    using the SQLite fts5 extension with the 'Unicode61' tokenizer.

    Notes:
        - this function assumes that 'database_path' points to an existing SQLite
    database already created with write_data_to_database() function.

    Args:
        database_path (Path): The path to the SQLite database file.
        accepted_special_characters (str): A string containing unicode characters
        that should be considered token characters by the tokenizer.
    Returns:
        None
    """
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

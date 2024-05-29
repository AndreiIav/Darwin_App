import sqlite3
from pathlib import Path

from flask import current_app

from application.cli_database.logic import (
    create_database,
    get_data_from_csv_file,
    write_to_database,
)


class TestCreateDatabase:

    def test_create_database_file_is_created(self, tmp_path):

        path_database = tmp_path / "test.db"

        create_database(path_database)

        assert path_database.is_file()

    def test_create_database_creates_correct_tables(self, tmp_path):

        path_database = tmp_path / "test.db"
        tables_to_be_created = [
            "magazines",
            "magazine_year",
            "magazine_number",
            "magazine_number_content",
        ]

        create_database(path_database)
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        tables = c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        existing_tables = [t[0] for t in tables]

        for table in tables_to_be_created:
            assert table in existing_tables


class TestGetDataFromCsv:

    def test_get_data_from_csv_reads_data_correctly(self, test_client):

        root_folder = Path(current_app.config["ROOT_FOLDER"])
        file_path = root_folder / "tests" / "test_data" / "create_db_test_data.csv"

        res = get_data_from_csv_file(file_path)

        assert res == [
            ("test_data_1", "test_data_2", "test_data_3", "test_data_4"),
            ("test_data_5", "test_data_6", "test_data_7", "test_data_8"),
        ]


class TestWriteToDatabase:

    def test_write_to_database_in_magazines_table(self, create_test_db):

        path_database = create_test_db
        test_data = [
            (1, "magazine_name_1", "magazine_link_1"),
            (2, "magazine_name_2", "magazine_link_2"),
        ]

        write_to_database(path_database, "magazines", test_data)

        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazines").fetchall()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]

    def test_write_to_database_in_magazine_year_table(
        self, create_test_db, insert_data_in_magazines_table
    ):

        path_database = create_test_db
        test_data = [
            (1, 1, "year_1", "year_link_1"),
            (2, 1, "year_2", "year_link_2"),
        ]

        write_to_database(path_database, "magazine_year", test_data)

        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazine_year").fetchall()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]

    def test_write_to_database_in_magazine_number_table(
        self, create_test_db, insert_data_in_magazine_year_table
    ):

        path_database = create_test_db
        test_data = [
            (1, 1, "number_1", "number_link_1"),
            (2, 1, "number_2", "number_link_2"),
        ]

        write_to_database(path_database, "magazine_number", test_data)

        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazine_number").fetchall()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]

    def test_write_to_database_in_magazine_magazine_number_content_table(
        self, create_test_db, insert_data_in_magazine_number_table
    ):

        path_database = create_test_db
        test_data = [
            (1, 1, "magazine_content_1", "magazine_page_1"),
            (2, 1, "magazine_content_2", "magazine_page_2"),
        ]

        write_to_database(path_database, "magazine_number_content", test_data)

        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazine_number_content").fetchall()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]

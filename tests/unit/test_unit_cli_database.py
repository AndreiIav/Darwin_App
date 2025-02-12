import sqlite3
from pathlib import Path

import pytest
from flask import current_app

from application.cli_database.cli_data_repository import (
    create_database,
    create_fts_table,
    create_magazine_details_table,
    get_data_from_csv_file,
    write_data_to_database,
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
        conn.close()

        existing_tables = [t[0] for t in tables]

        for table in tables_to_be_created:
            assert table in existing_tables


class TestGetDataFromCsv:
    def test_get_data_from_csv_reads_data_correctly(self, test_client):
        files_path = Path(current_app.config["DATABASE_FILES"])
        file_path = files_path / "get_data_from_csv_test_data.csv"

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
        conn.close()

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
        conn.close()

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
        conn.close()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]

    def test_write_to_database_in_magazine_magazine_number_content_table(
        self, create_test_db, insert_data_in_magazine_number_table
    ):
        path_database = create_test_db
        test_data = [
            (1, 1, "magazine_content_1", 1),
            (2, 1, "magazine_content_2", 2),
        ]

        write_to_database(path_database, "magazine_number_content", test_data)

        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazine_number_content").fetchall()
        conn.close()

        for row in range(len(test_data)):
            for column in range(len(test_data[row])):
                assert test_data[row][column] == inserted_data[row][column]


class TestWriteDataToDatabase:
    def test_write_data_to_database(self, test_client, create_test_db):
        files_path = Path(current_app.config["DATABASE_FILES"])
        database_path = create_test_db
        files_to_tables = current_app.config["FILES_TO_TABLES"]

        write_data_to_database(files_path, database_path, files_to_tables)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        magazines_inserted_data = c.execute("SELECT * FROM magazines").fetchall()
        magazine_year_inserted_data = c.execute(
            "SELECT * FROM magazine_year"
        ).fetchall()
        magazine_number_inserted_data = c.execute(
            "SELECT * FROM magazine_number"
        ).fetchall()
        magazine_number_content_data = c.execute(
            "SELECT * FROM magazine_number_content"
        ).fetchall()
        conn.close()

        assert magazines_inserted_data == [
            (1, "magazine_name_1", "magazine_link_1"),
            (2, "magazine_name_2", "magazine_link_2"),
        ]
        assert magazine_year_inserted_data == [
            (1, 1, "year_1", "year_link_1"),
            (2, 1, "year_2", "year_link_2"),
        ]
        assert magazine_number_inserted_data == [
            (1, 1, "number_1", "number_link_1"),
            (2, 1, "number_2", "number_link_2"),
        ]
        assert magazine_number_content_data == [
            (1, 1, "magazine_content_1", 1),
            (2, 1, "magazine_content_2", 2),
        ]

    def test_write_data_to_database_with_missing_file_raises_error(
        self, test_client, create_test_db
    ):
        files_path = Path(current_app.config["DATABASE_FILES"])
        database_path = create_test_db
        missing_file = "fake_name"
        files_to_tables = [
            (f"{missing_file}", "magazines"),
        ]

        with pytest.raises(FileNotFoundError) as err:
            write_data_to_database(files_path, database_path, files_to_tables)

        assert "FileNotFoundError" and missing_file in str(err)


class TestCreateMagazineDetailsTable:
    def test_create_magazine_details_table_created(
        self, insert_data_in_magazine_number_content_table
    ):
        database_path = insert_data_in_magazine_number_content_table

        create_magazine_details_table(database_path)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        inserted_data = c.execute("SELECT * FROM magazine_details").fetchall()
        conn.close()

        assert inserted_data == [(1, 1, "year_1", 1, 2)]


class TestCreateFtsTable:
    def test_create_fts_table_with_match_query(
        self, insert_data_in_magazine_number_content_table
    ):
        database_path = insert_data_in_magazine_number_content_table

        create_fts_table(database_path)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        inserted_data = c.execute(
            """
        SELECT *
        FROM magazine_number_content mnc
        INNER JOIN magazine_number_content_fts mncf ON mnc.id = mncf.rowid
        WHERE magazine_number_content_fts MATCH '"magazine_content"*'
           """
        ).fetchall()
        conn.close()

        assert len(inserted_data) == 2

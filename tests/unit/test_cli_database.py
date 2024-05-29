import sqlite3
from pathlib import Path

import pytest
from flask import current_app

from application.cli_database.logic import create_database, get_data_from_csv_file


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

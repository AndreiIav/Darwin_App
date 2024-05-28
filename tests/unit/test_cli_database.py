import sqlite3

from application.cli_database.logic import create_database


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

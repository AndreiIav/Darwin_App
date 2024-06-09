import sqlite3

import pytest


@pytest.mark.parametrize("database_name", ["test", "demo"])
def test_cli_create_database_correct(
    test_cli_app, database_name, monkeypatch, tmp_path
):

    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)

    path_database = tmp_path / f"{database_name}.db"

    runner = test_cli_app.test_cli_runner()
    runner.invoke(args=["database", "create", database_name])

    tables_to_be_created = [
        "magazines",
        "magazine_year",
        "magazine_number",
        "magazine_number_content",
        "magazine_details",
        "magazine_number_content_fts",
    ]

    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    existing_tables = [t[0] for t in tables]

    for table in tables_to_be_created:
        assert table in existing_tables

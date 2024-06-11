import sqlite3

import pytest
import click


@pytest.mark.parametrize("database_name", ["test", "demo"])
def test_cli_create_database_correct_tables_and_data(
    test_cli_app, database_name, monkeypatch, tmp_path
):

    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_folder = test_cli_app.config["DATABASE_FOLDER"]

    runner = test_cli_app.test_cli_runner()
    runner.invoke(args=["database", "create", database_name])

    path_database = database_folder / f"{database_name}.db"
    conn = sqlite3.connect(path_database)
    c = conn.cursor()

    magazines_inserted_data = c.execute("SELECT * FROM magazines").fetchall()
    magazine_year_inserted_data = c.execute("SELECT * FROM magazine_year").fetchall()
    magazine_number_inserted_data = c.execute(
        "SELECT * FROM magazine_number"
    ).fetchall()
    magazine_number_content_inserted_data = c.execute(
        "SELECT * FROM magazine_number_content"
    ).fetchall()
    magazine_details_inserted_data = c.execute(
        "SELECT * FROM magazine_details"
    ).fetchall()
    fts_table_inserted_data = c.execute(
        """
        SELECT *
        FROM magazine_number_content mnc
        INNER JOIN magazine_number_content_fts mncf ON mnc.id = mncf.rowid
        WHERE magazine_number_content_fts MATCH '"magazine_content"*'
           """
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
    assert magazine_number_content_inserted_data == [
        (1, 1, "magazine_content_1", 1),
        (2, 1, "magazine_content_2", 2),
    ]
    assert magazine_details_inserted_data == [(1, 1, "year_1", 1, 2)]
    assert len(fts_table_inserted_data) == 2


@pytest.mark.parametrize("database_name", ["test", "demo"])
def test_cli_create_database_correct_confirmation_message(
    test_cli_app, database_name, monkeypatch, tmp_path
):

    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_folder = test_cli_app.config["DATABASE_FOLDER"]

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "create", database_name])

    standard_output = res.stdout

    assert f"database {database_name} created in {database_folder}" in standard_output


def test_cli_create_database_with_incorrect_database_name(test_cli_app):

    database_name = "wrong_name"

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "create", database_name])

    assert res.exit_code == 2
    assert f"Error: Invalid value: {database_name}" in res.output


def test_cli_create_database_with_already_existing_database_file(
    test_cli_app, monkeypatch, tmp_path
):

    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_folder = test_cli_app.config["DATABASE_FOLDER"]
    database_name = "test"
    database_path = database_folder / f"{database_name}.db"

    # create a sqlite3 .db file
    conn = sqlite3.connect(database_path)
    conn.close()

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "create", database_name])

    assert res.exit_code == 2
    assert f"{database_name} database already exists." in res.output


def test_cli_remove_database_file_deletes_database(test_cli_app, monkeypatch, tmp_path):

    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_folder = test_cli_app.config["DATABASE_FOLDER"]
    database_name = "test"
    database_path = database_folder / f"{database_name}.db"

    # create a sqlite3 .db file
    conn = sqlite3.connect(database_path)
    conn.close()

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "remove", database_name])

    assert f"{database_name} database was removed from {database_folder}" in res.output

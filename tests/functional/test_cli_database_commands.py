import sqlite3

import pytest

import application

# -------------------------------
# create_new_database command tests
# -------------------------------


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


def test_cli_create_database_with_incorrect_database_name_argument(test_cli_app):
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


def test_cli_create_database_with_missing_database_name_argument(test_cli_app):
    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "create"])

    assert res.exit_code == 2
    assert "Error: Missing argument 'NAME'." in res.output


def test_cli_create_database_handles_FileNotFoundError(
    test_cli_app, monkeypatch, tmp_path
):
    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    missing_file = "missing_file.csv"

    def fake_write_data_to_database(a, b, c):
        raise FileNotFoundError(f"{missing_file}")

    # Monkeypatch write_data_to_database() to one that
    # raises FileNotFoundError error
    monkeypatch.setattr(
        application.cli_database.cli,
        "write_data_to_database",
        fake_write_data_to_database,
    )

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "create", "demo"])

    assert (
        "The file needed to create the"
        " database was not found.\n"
        "Check the csv files and try again.\n"
        "If a database file was already created use"
        " 'flask database remove <name_of_database>'"
        " command to delete it."
    ) in res.output


# --------------------------------
# remove_database_file command tests
# --------------------------------


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


def test_cli_remove_database_file_to_be_removed_does_not_exist(
    test_cli_app, monkeypatch, tmp_path
):
    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_name = "test"

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "remove", database_name])

    assert res.exit_code == 2
    assert f"{database_name} database does not exist." in res.output


def test_cli_remove_database_file_with_incorrect_database_name(
    test_cli_app, monkeypatch, tmp_path
):
    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(test_cli_app.config, "DATABASE_FOLDER", tmp_path)
    database_name = "wrong_name"

    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "remove", database_name])

    assert res.exit_code == 2
    assert f"Error: Invalid value: {database_name}" in res.output


def test_cli_remove_database_with_missing_database_name_argument(test_cli_app):
    runner = test_cli_app.test_cli_runner()
    res = runner.invoke(args=["database", "remove"])

    assert res.exit_code == 2
    assert "Error: Missing argument 'NAME'." in res.output

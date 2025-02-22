import os
from pathlib import Path

import click
from flask import Blueprint, current_app

from application.cli_database.cli_data_repository import (
    create_database,
    create_fts_table,
    create_magazine_details_table,
    write_data_to_database,
)

# Blueprint Configuration
cli_database_bp = Blueprint("cli_database_bp", __name__, cli_group="database")
"""
Blueprint: cli_database_bp
This blueprint provides custom commands to create and delete a SQLite database
file.
"""


@cli_database_bp.cli.command("create")
@click.argument("name")
def create_new_database(name):
    """
    Create and populate a new SQLite database file.

    This command creates and populates a new SQLite database file with the
    provided name.
    The accepted names are: "test", "demo".
    The database is populated with data so it can be used for testing or demo
    purposes.

    Args:
        name (str): The name of the database file to be created.

    Returns:
        None

    Raises:
        click.BadParameter: If the provided database name is not valid.
        click.UsageError: If a SQLite file with the provided name already
            exists.
        click.FileError: If a CSV file needed to populate the database is
            missing.
    """
    if name not in ("test", "demo"):
        raise click.BadParameter(name)

    database_name = f"{name}.db"
    database_folder = Path(current_app.config["DATABASE_FOLDER"])
    database_path = database_folder / database_name
    create_database_files_path = Path(current_app.config["DATABASE_FILES"])
    files_to_tables = current_app.config["FILES_TO_TABLES"]
    accepted_special_characters = current_app.config["ACCEPTED_FTS5_SPECIAL_CHARACTERS"]

    # check if a database file with the requested name already exists
    if database_path.is_file():
        raise click.UsageError(message=f"{name} database already exists.")

    # create database
    create_database(database_path)

    # populate database
    try:
        write_data_to_database(
            create_database_files_path, database_path, files_to_tables
        )
    except FileNotFoundError as e:
        error_message = str(e)
        raise click.FileError(
            error_message,
            hint="The file needed to create the"
            " database was not found.\n"
            "Check the csv files and try again.\n"
            "If a database file was already created use"
            " 'flask database remove <name_of_database>'"
            " command to delete it.",
        )

    # create and populate magazine_details table
    create_magazine_details_table(database_path)

    # create and populate the fts table
    create_fts_table(
        database_path, accepted_special_characters=accepted_special_characters
    )

    print(f"database {name} created in {database_folder}")


@cli_database_bp.cli.command("remove")
@click.argument("name")
def remove_database_file(name):
    """
    Delete SQLite database file.

    This command deletes the SQLite database file with the provided name. The
    accepted names are: "test", "demo".

    Args:
        name (str): The name of the database file to be deleted.

    Returns:
        None

    Raises:
        click.BadParameter: If the provided name is not valid.
        click.UsageError: If a SQLite file with the provided name doesn't
        exists.
    """
    if name not in ("test", "demo"):
        raise click.BadParameter(name)

    database_name = f"{name}.db"
    database_folder = Path(current_app.config["DATABASE_FOLDER"])
    database_path = database_folder / database_name

    # check if a database file with the requested name exists to be deleted
    # and, if not, raise an error
    if not database_path.is_file():
        raise click.UsageError(message=f"{name} database does not exist.")

    # delete database file
    os.remove(database_path)

    print(f"{name} database was removed from {database_folder}")

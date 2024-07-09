import os
from pathlib import Path

import click
from flask import Blueprint, current_app

from application.cli_database.logic import (
    create_database,
    create_fts_table,
    create_magazine_details_table,
    write_data_to_database,
)

# Blueprint Configuration
cli_database_bp = Blueprint("cli_database_bp", __name__, cli_group="database")


@cli_database_bp.cli.command("create")
@click.argument("name")
def create_new_database(name):
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
    write_data_to_database(create_database_files_path, database_path, files_to_tables)

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

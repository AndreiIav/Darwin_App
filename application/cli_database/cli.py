from pathlib import Path

from flask import Blueprint, current_app
import click

from application.cli_database.logic import (
    create_database,
    write_data_to_database,
    create_magazine_details_table,
    create_fts_table,
)


# Blueprint Configuration
cli_database_bp = Blueprint("cli_database_bp", __name__, cli_group="database")


@cli_database_bp.cli.command("create")
@click.argument("name")
def create_new_database(name):

    if name not in ("test", "demo"):
        raise click.BadParameter(name)

    if name == "test":
        database_name = "test.db"
    elif name == "demo":
        database_name = "app.db"

    root_folder = Path(current_app.config["ROOT_FOLDER"])
    database_path = root_folder / "instance" / database_name
    create_database_files_path = (
        root_folder / "application" / "cli_database" / "create_database_files"
    )
    files_to_tables = [
        ("magazines.csv", "magazines"),
        ("magazine_years.csv", "magazine_year"),
        ("magazine_numbers.csv", "magazine_number"),
        ("magazine_content.csv", "magazine_number_content"),
    ]

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
    create_fts_table(database_path)

    print(f"database {name} created at {database_path}")

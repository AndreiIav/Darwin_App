import sqlite3


import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(sqlite3.connect("test.db"))
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

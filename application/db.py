import sqlite3
import os
from flask import g


def get_db():
    if "db" not in g:
        db_path = os.path.join("D:\IT projects\Darwin_App", "test.db")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row

    return g.db

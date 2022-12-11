from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def search_page():
    if request.method == "GET":
        return render_template("search_page.html")
    if request.method == "POST":
        s_word = request.form.get("search_term", "default")

        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        c.execute(
            "SELECT COUNT(*) FROM magazine_number_content WHERE magazine_content LIKE :word",
            {"word": "%" + s_word + "%"},
        )
        res = c.fetchone()[0]
        conn.close()

        return render_template("search_page.html", searched=s_word, res=res)

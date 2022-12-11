from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def search_page():
    return render_template("search_page.html")


@app.route("/searched_word", methods=["POST"])
def searched_word():
    s_word = request.form.get("search_term", "default")
    return render_template("searched_word.html", searched=s_word)

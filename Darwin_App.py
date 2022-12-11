from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def search_page():
    if request.method == "GET":
        return render_template("search_page.html")
    if request.method == "POST":
        s_word = request.form.get("search_term", "default")
        return render_template("searched_word.html", searched=s_word)

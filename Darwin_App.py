from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def search_page():
    return render_template("search_page.html")

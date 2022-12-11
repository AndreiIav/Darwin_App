from flask import Flask, render_template, jsonify, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def search_page():
    return render_template("search_page.html")


@app.route("/searched_word/<searched_word>")
def searched_word(searched_word):
    return render_template("searched_word.html", searched=searched_word)

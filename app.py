"""Munch Flask App"""
from flask import Flask, render_template
from utilities import get_dhalls

app = Flask(__name__)


@app.route("/")
def index():
    """Render Homepage"""
    return render_template("index.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/entree-select")
def entree_select():
    return render_template("entree-select.html")


@app.route("/dhall-select")
def select_dhall():
    """Start rate process by rendering dining hall selector"""
    dhalls = get_dhalls()
    return render_template("dhall-select.html", dhalls=dhalls)


@app.route("/menu")
def menu():
    return render_template("index.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.route("/about")
def about():
    return render_template("about.html")

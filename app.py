"""Munch Flask App"""
import datetime
from flask import Flask, render_template, request
from utilities import get_dhalls, get_menu

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


@app.route("/review")
def review():
    """Show review form for user to write review"""

    location_id = request.args.get("location")

    menu = get_menu(location=location_id, meal=3)

    entrees = [item for item in menu if item["Menu_Category_Name"] == "Entrees"]
    soups = [item for item in menu if item["Menu_Category_Name"] == "Today's Soup"]

    return render_template("review.html", entrees=entrees, soups=soups)


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

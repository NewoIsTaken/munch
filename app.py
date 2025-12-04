"""Munch Flask App"""
import datetime
from datetime import datetime
from flask import Flask, redirect, render_template, request
from utilities import get_dhalls, get_menu, lunch_time, dinner_time

app = Flask(__name__)

# Setup variables to store the menu so we don't have to fetch it every time.
lunch = {
    "fetched_on": "",
    "entrees": [],
    "soups": []
}

dinner = {
    "fetched_on": "",
    "entrees": [],
    "soups": []
}


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

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    if lunch_time():
        if lunch["fetched_on"] != date_string:
            lunch.update(get_menu(location=location_id, meal=2))

        return render_template("review.html", entrees=lunch["entrees"], soups=lunch["soups"])

    elif dinner_time():
        if dinner["fetched_on"] != date_string:
            dinner.update(get_menu(location=location_id, meal=3))

        return render_template("review.html", entrees=dinner["entrees"], soups=dinner["soups"])

    else:
        return redirect("/reviews")

    # If dinner menu has not been fetched, fetch it and update the dinner dict


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

"""Munch Flask App"""
import datetime
from datetime import datetime
from flask import Flask, redirect, render_template, request
from utilities import get_dhalls, get_menu, lunch_time, dinner_time

app = Flask(__name__)

# Setup variables to store the menu so we don't have to fetch it every time.
location = []

for i in range(99):
    location.append({
        "lunch": {
            "fetched_on": "",
            "entrees": [],
            "soups": []
        },
        "dinner": {
            "fetched_on": "",
            "entrees": [],
            "soups": []
        }
    })


@app.route("/")
def index():
    """Render Homepage"""
    return render_template("index.html")


@app.route("/review")
def review():
    """Show review form for user to write review"""
    # TODO: add check to make sure this user has yet to review this meal at this DHall

    location_id = int(request.args.get("location"))

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    if lunch_time():
        if location[location_id]["lunch"]["fetched_on"] != date_string:
            location[location_id]["lunch"].update(
                get_menu(location=location_id, meal=2))

        return render_template("review.html", dishes=location[location_id]["lunch"], meal_name="Lunch", meal_date=date_string, location=location_id)

    elif dinner_time():
        if location[location_id]["dinner"]["fetched_on"] != date_string:
            location[location_id]["dinner"].update(
                get_menu(location=location_id, meal=3))

        return render_template("review.html", dishes=location[location_id]["dinner"], meal_name="Dinner", meal_date=date_string, location=location_id)

    else:
        return redirect("/reviews")

    # If dinner menu has not been fetched, fetch it and update the dinner dict


@app.route("/dhall-select")
def select_dhall():
    """Start rate process by rendering dining hall selector"""
    dhalls = get_dhalls()
    return render_template("dhall-select.html", dhalls=dhalls)


@app.route("/rate", methods=["POST"])
def process_rating():
    """Take in rating information from form, process it, and store it"""
    ratings = {}
    location_id = int(request.form.get("location"))

    if lunch_time():
        for category in location[location_id]["lunch"]:
            if category == "fetched_on":
                continue

            for dish in location[location_id]["lunch"][category]:
                try:
                    rating = int(request.form.get(
                        dish["Recipe_Print_As_Name"]))
                except ValueError:
                    continue

                ratings[dish["Recipe_Print_As_Name"]] = rating

    elif dinner_time():
        for category in location[location_id]["dinner"]:
            if category == "fetched_on":
                continue

            for dish in location[location_id]["dinner"][category]:
                try:
                    rating = int(request.form.get(
                        dish["Recipe_Print_As_Name"]))
                except ValueError:
                    continue
                ratings[dish["Recipe_Print_As_Name"]] = rating

    print(ratings)

    return redirect("/")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/about")
def about():
    return render_template("about.html")

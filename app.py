"""Munch Flask App"""

import datetime
from datetime import datetime, time
import sqlite3
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

    # Get location_id for the location we're making this review for
    try:
        location_id = int(request.args.get("location"))
    except TypeError:
        return "No location provided"

    # Get the current date as MM/DD/YYYY
    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    if lunch_time():
        meal_name = "lunch"
        meal_id = 2

    elif dinner_time():
        meal_name = "dinner"
        meal_id = 3

    else:
        return redirect("/reviews?location=" + location_id)

    # If the menu for this meal for this location selected has yet to be fetched today, do so
    if location[location_id][meal_name]["fetched_on"] != date_string:
        response = get_menu(location=location_id, meal=meal_id)

        # Check to make sure good response from API, if not, return the response code.
        if not isinstance(response, dict):
            return response

        # Update cache with the new menu
        location[location_id][meal_name] = response

    # Now, render the review screen with this info.
    return render_template("review.html",
                           dishes=location[location_id][meal_name],
                           meal_name=meal_name.capitalize(), meal_date=date_string,
                           location=location_id)


@app.route("/dhall-select")
def select_dhall():
    """Render dining hall selection form and then redirect user to the appropriate page."""
    # Get the location where we want to go after we select dining hall
    redirect_location = request.args.get("redirect")

    # Get the list of dining halls
    dhalls = get_dhalls()
    return render_template("dhall-select.html", dhalls=dhalls, redirect=redirect_location)


@app.route("/rate", methods=["POST"])
def process_rating():
    """Take in rating information from form, process it, and store it"""
    # Get the location for which we are rating
    try:
        location_id = int(request.args.get("location"))
    except TypeError:
        return "No location provided"

    # Create DB connection to the SQLite db
    db_connection = sqlite3.connect("munch.db")
    db_cursor = db_connection.cursor()

    # Get the current date as DD/MM/YYYY
    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    if lunch_time():
        meal_name = "lunch"
        meal_id = 2

    elif dinner_time():
        meal_name = "dinner"
        meal_id = 3

    else:
        return "It is not currently a meal time so we can not process your rating."

    # For each category of dish
    for category in location[location_id][meal_name]:
        # Skip if this is the fetched_on field
        if category == "fetched_on":
            continue

        # For each dish from the menu of the category
        for dish in location[location_id][meal_name][category]:
            # Try to get the form rating of this dish
            try:
                rating = int(request.form.get(
                    dish["Recipe_Print_As_Name"]))
            # If the rating is not a number, go to the next menu item.
            except ValueError:
                continue

            # Insert this rating into the DB
            query = "INSERT INTO ratings VALUES (?, ?, ?, ?, ?)"
            db_cursor.execute(
                query, (dish["Recipe_Print_As_Name"], rating, date_string, location_id, meal_id))
            db_connection.commit()

    db_cursor.close()
    db_connection.close()

    return redirect("/reviews?location=" + str(location_id))


@app.route("/reviews")
def reviews():
    """Display the current reviews"""
    # Get the location for which we are trying to get the reviews for
    try:
        location_id = int(request.args.get("location"))
    except TypeError:
        return "No location provided"

    # Get the current date as MM/DD/YYYY
    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    # Establish DB connection
    db_connection = sqlite3.connect("munch.db")
    db_cursor = db_connection.cursor()

    # Determine the current meal or the meal that last ended
    if lunch_time(end=time(16, 30)):
        meal = 2

    elif dinner_time(end=time(11, 30)):
        meal = 3

    else:
        meal = 3

    # Query the DB for the appropriate rating information
    query = """SELECT dish, AVG(rating) FROM ratings
    WHERE date = ? AND location = ? AND meal = ?
    GROUP BY dish"""
    result = db_cursor.execute(query, (date_string, location_id, meal))
    data = result.fetchall()

    # Close the DB connection
    db_cursor.close()
    db_connection.close()

    # If no data available yet, tell the user.
    if len(data) == 0:
        return render_template("reviews.html", error="No data available yet! Come back later!")

    return render_template("reviews.html", data=data)


@app.route("/menu")
def menu():
    """Get menu info and render it"""
    # Get the location_id for the location we are trying to query for
    try:
        location_id = int(request.args.get("location"))
    except TypeError:
        return "No location provided"

    # Get the current date as MM/DD/YYYY
    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    # check if we already have a current lunch menu fetched. if not, update our cache
    if location[location_id]["lunch"]["fetched_on"] != date_string:
        response = get_menu(location=location_id, meal=2)
        if not isinstance(response, dict):
            return response
        location[location_id]["lunch"] = response

    # check if we already have a current dinner menu fetched. if not, update our cache
    if location[location_id]["dinner"]["fetched_on"] != date_string:
        response = get_menu(location=location_id, meal=3)
        if not isinstance(response, dict):
            return response
        location[location_id]["dinner"] = response

    return render_template("menu.html",
                           lunch=location[location_id]["lunch"],
                           dinner=location[location_id]["dinner"],
                           meal_date=date_string, location=location_id)


@app.route("/about")
def about():
    """Render about page"""
    return render_template("about.html")

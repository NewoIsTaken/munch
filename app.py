"""Munch Flask App"""

# Munch: an app to streamline the Harvard University Dining Services
# menu and allow students to rate and view others' ratings of their
# dining hall's food
#
# Copyright (C) 2025  Brian Tollar, Brody Van Wave, Owen Wang

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

    location_id = int(request.args.get("location"))

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    if lunch_time():
        # check if we already have a current lunch menu fetched
        if location[location_id]["lunch"]["fetched_on"] != date_string:
            location[location_id]["lunch"].update(
                get_menu(location=location_id, meal=2))

        return render_template("review.html",
                               dishes=location[location_id]["lunch"],
                               meal_name="Lunch", meal_date=date_string, location=location_id)

    elif dinner_time():
        # check if we already have a current dinner menu fetched
        if location[location_id]["dinner"]["fetched_on"] != date_string:
            location[location_id]["dinner"].update(
                get_menu(location=location_id, meal=3))

        return render_template("review.html",
                               dishes=location[location_id]["dinner"],
                               meal_name="Dinner", meal_date=date_string, location=location_id)

    else:
        return redirect("/reviews")

    # If dinner menu has not been fetched, fetch it and update the dinner dict


@app.route("/dhall-select")
def select_dhall():
    """Start rate process by rendering dining hall selector"""
    redirect_location = request.args.get("redirect")
    dhalls = get_dhalls()
    return render_template("dhall-select.html", dhalls=dhalls, redirect=redirect_location)


@app.route("/rate", methods=["POST"])
def process_rating():
    """Take in rating information from form, process it, and store it"""
    ratings = {}
    location_id = int(request.form.get("location"))

    db_connection = sqlite3.connect("munch.db")
    db_cursor = db_connection.cursor()
    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

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

                query = "INSERT INTO ratings VALUES (?, ?, ?, ?, 2)"
                db_cursor.execute(
                    query, (dish["Recipe_Print_As_Name"], rating, date_string, location_id))
                db_connection.commit()

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
                query = "INSERT INTO ratings VALUES (?, ?, ?, ?, 3)"
                db_cursor.execute(
                    query, (dish["Recipe_Print_As_Name"], rating, date_string, location_id))
                db_connection.commit()

    db_cursor.close()
    db_connection.close()

    return redirect("/reviews?location=" + location_id)


@app.route("/reviews")
def reviews():
    """Display the current reviews"""
    location_id = int(request.args.get("location"))

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    db_connection = sqlite3.connect("munch.db")
    db_cursor = db_connection.cursor()

    if lunch_time(end=time(16, 30)):
        meal = 2

    elif dinner_time(end=time(11, 30)):
        meal = 3

    else:
        meal = 2

    query = """SELECT dish, AVG(rating) FROM ratings
    WHERE date = ? AND location = ? AND meal = ?
    GROUP BY dish"""
    result = db_cursor.execute(query, (date_string, location_id, meal))
    data = result.fetchall()

    db_cursor.close()
    db_connection.close()

    error = ""
    if len(data) == 0:
        error = "No data available yet! Come back later!"

    return render_template("reviews.html", data=data, error=error)


@app.route("/menu")
def menu():
    """Get menu info and render it"""
    location_id = int(request.args.get("location"))

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    # check if we already have a current lunch menu fetched
    if location[location_id]["lunch"]["fetched_on"] != date_string:
        location[location_id]["lunch"].update(
            get_menu(location=location_id, meal=2))

    # check if we already have a current dinner menu fetched
    if location[location_id]["dinner"]["fetched_on"] != date_string:
        location[location_id]["dinner"].update(
            get_menu(location=location_id, meal=3))

    return render_template("menu.html",
                           lunch=location[location_id]["lunch"],
                           dinner=location[location_id]["dinner"],
                           meal_date=date_string, location=location_id)


@app.route("/about")
def about():
    """Render about page"""
    return render_template("about.html")

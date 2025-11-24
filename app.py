from flask import Flask, render_template
import json
import os
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/entree-select")
def entree_select():
    return render_template("entree-select.html")


@app.route("/rate")
def rate():
    return render_template("rate.html")


def load_menu_json():
    menu_path = Path(app.root_path) / "data" / "menu_today.json"
    if menu_path.exists():
        with menu_path.open(encoding="utf-8") as f:
            return json.load(f)
    return None

@app.route("/menu/lunch")
def menu_lunch():
    data = load_menu_json()
    menu_data = None
    if data:
        menu_data = {
            "date": data.get("date"),
            "categories": data.get("lunch", []),
        }
    return render_template("menu_meal.html", menu=menu_data, meal_name="Lunch")

@app.route("/menu/dinner")
def menu_dinner():
    data = load_menu_json()
    menu_data = None
    if data:
        menu_data = {
            "date": data.get("date"),
            "categories": data.get("dinner", []),
        }
    return render_template("menu_meal.html", menu=menu_data, meal_name="Dinner")

    

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.route("/about")
def about():
    return render_template("about.html")

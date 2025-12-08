"""Module with utilites for fetching things from HUDS's API"""

from functools import wraps
import os
from datetime import datetime, time
from flask import redirect, request, session, url_for
import pytz
import requests
from dotenv import load_dotenv

# HUIT Dining API URL
URL = "https://go.apis.huit.harvard.edu/ats/dining/v3/"

# Load .env file and get the API_KEY env variable and set it as a header for the API requests
load_dotenv()
API_KEY = os.getenv("API_KEY")
headers = {
    "X-Api-Key": API_KEY
}

categories = ["Entrees", "Today's Soup", "Desserts"]


def get_dhalls():
    """Get and return list of dining halls from HUDS's API"""
    # API Request building
    endpoint = "locations"

    response = requests.get(url=URL + endpoint, headers=headers, timeout=100)

    if response.status_code != 200:
        return response.status_code

    # Response from API
    dhalls = response.json()

    # Clean up the list of HUDS locations to only the house dining halls and Berg
    clean_list = [dhall for dhall in dhalls
                  if "Hall" in dhall["location_name"]
                  or "House" in dhall["location_name"]]

    return clean_list

# Location is the HUDS API two digit location ID
# Meal is breakfast, lunch, and dinner passed in as 1, 2, and 3
# Date is the date of menu to return, by default today's


def get_menu(location, meal, date=datetime.now(pytz.timezone('America/New_York'))):
    """Get and return menu items given the dining hall location ID"""

    # API Request building
    endpoint = "recipes"
    params = {
        "locationId": f'{location:02}'
    }

    # Make API Request
    response = requests.get(
        url=URL + endpoint, params=params, headers=headers, timeout=100)

    if response.status_code != 200:
        return response.status_code

    # Get response
    items = response.json()

    # Get the current date as MM/DD/YYYY
    date_string = date.strftime("%m/%d/%Y")

    # Clean the list of dishes to only include those of today and of the meal specified
    clean_list = [item for item in items
                  if item["Serve_Date"] == date_string
                  and item["Meal_Number"] == meal]

    # Format the API response into our dictionary.
    meal_dict = {
        "fetched_on": date_string
    }

    for category in categories:
        meal_dict[category] = [
            item for item in clean_list if item["Menu_Category_Name"] == category]

    return meal_dict


# Start is the start time of lunch, by default 11:30
# End is the end time of lunch, by default when dinner starts at 4:30
# The time we want to query if lunchtime is the time now
def lunch_time(start=time(11, 30), end=time(16, 30), now=datetime.now(pytz.timezone('America/New_York')).time()):
    """Check if current time is during dinner"""
    now = now or datetime.now(pytz.timezone('America/New_York')).time()
    # handles ranges that do not cross midnight
    if start <= end:
        return start <= now <= end
    # handles ranges that cross midnight (e.g., 22:00–02:00)
    return now >= start or now <= end


# Start is the start time of dinner, by default 4:30
# End is the end time of dinner, by default when dinner starts at 7:30
# The time we want to query if dinnertime is the time now
def dinner_time(start=time(16, 30), end=time(19, 30), now=datetime.now(pytz.timezone('America/New_York')).time()):
    """Check if current time is during dinner"""
    now = now or datetime.now(pytz.timezone('America/New_York')).time()
    # handles ranges that do not cross midnight
    if start <= end:
        return start <= now <= end
    # handles ranges that cross midnight (e.g., 22:00–02:00)
    return now >= start or now <= end


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userinfo") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

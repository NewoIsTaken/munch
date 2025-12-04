"""Module with utilites for fetching things from HUDS's API"""

import os
from datetime import datetime, time
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://go.apis.huit.harvard.edu/ats/dining/v3/"
API_KEY = os.getenv("API_KEY")
headers = {
    "X-Api-Key": API_KEY
}


def get_dhalls():
    """Get and return list of dining halls from HUDS's API"""
    endpoint = "locations"

    response = requests.get(url=URL + endpoint, headers=headers, timeout=100)

    dhalls = response.json()

    clean_list = [dhall for dhall in dhalls
                  if "Hall" in dhall["location_name"]
                  or "House" in dhall["location_name"]]

    return clean_list


def get_menu(location, meal):
    """Get and return menu items given the dining hall location ID"""
    endpoint = "recipes"

    params = {
        "locationId": location
    }

    response = requests.get(
        url=URL + endpoint, params=params, headers=headers, timeout=100)

    items = response.json()

    date = datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    clean_list = [item for item in items
                  if item["Serve_Date"] == date_string
                  and item["Meal_Number"] == meal]

    meal_dict = {
        "fetched_on": date_string,
        "entrees": [item for item in clean_list if item["Menu_Category_Name"] == "Entrees"],
        "soups": [item for item in clean_list if item["Menu_Category_Name"] == "Today's Soup"]
    }

    return meal_dict


def lunch_time(start=time(11, 30), end=time(2, 00), now=datetime.now().time()):
    """Check if current time is during dinner"""
    now = now or datetime.now().time()
    # handles ranges that do not cross midnight
    if start <= end:
        return start <= now <= end
    # handles ranges that cross midnight (e.g., 22:00–02:00)
    return now >= start or now <= end


def dinner_time(start=time(4, 30), end=time(7, 30), now=datetime.now().time()):
    """Check if current time is during dinner"""
    now = now or datetime.now().time()
    # handles ranges that do not cross midnight
    if start <= end:
        return start <= now <= end
    # handles ranges that cross midnight (e.g., 22:00–02:00)
    return now >= start or now <= end

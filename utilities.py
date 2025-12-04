"""Module with utilites for fetching things from HUDS's API"""

import os
import datetime
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

    date = datetime.datetime.now()
    date_string = date.strftime("%m/%d/%Y")

    clean_list = [item for item in items
                  if item["Serve_Date"] == date_string
                  and item["Meal_Number"] == meal]

    return clean_list

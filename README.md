# Munch

Munch is a web application that queries Harvard University Dining Service's (HUDS's) API to fetch menu info and provide a platform for Harvard students to rate their meals at their dining hall.

## Installation

### Project
This project uses [pipenv](https://pipenv.pypa.io/) to create a virtual environment and manage dependencies for the project.

The pipenv project's recommended method to install pipenv is to install it from the [`PyPI`](https://pypi.org/) with [`pip`](https://pip.pypa.io/):
```bash
pip install --user pipenv
```
For more information about installing pipenv, see their installation guide [here](https://pipenv.pypa.io/en/latest/installation.html).

After installing pipenv, clone a copy of this repo and in the root folder of this project, create the virtual environment and install the appropriate dependencies with `pipenv`:
```bash
pipenv install
```

### Harvard API Setup
Additionally, this project fetches the menu information from Harvard University Information Technology's (HUIT's) Dining API. However, in order to use this API, one must register an application with [HUIT's API portal](https://portal.apis.huit.harvard.edu/).

Then, one can find their application that they created on the [My Apps](https://portal.apis.huit.harvard.edu/my-apps) page. Clicking into the application, enable the Dining API in the API section. Then, an API key will be generated on the same page.

Create a duplicate of the `.env.example` file or rename it to `.env`. Paste the API key that you obtained from HUIT's API Portal into the indicated field.

## Usage
Once the virtual environment is created for this project, you can then start the Flask application.

By activating the virtual environment and then running the Flask app as normal:
```bash
pipenv shell
flask run
```
Or running the app in the virtual environment with `pipenv run`:
```bash
pipenv run flask run
```

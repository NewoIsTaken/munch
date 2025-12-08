# Munch

Munch is a web application that queries Harvard University Dining Service's (HUDS's) API to fetch menu info and provide a platform for Harvard students to rate their meals at their dining hall.

It is currently hosted at [munch-2wuw.onrender.com](https://munch-2wuw.onrender.com) if you would like to access it.

## Installation & Setup

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
Additionally, this project fetches the menu information from Harvard University Information Technology's (HUIT's) Dining API. However, in order to use this API, one must register an application with [HUIT's API portal](https://portal.apis.huit.harvard.edu/) after signing in. Only Harvard affiliates with HarvardKeys are allowed to do so.

To register an app, one can click on the new app button on the [My Apps](https://portal.apis.huit.harvard.edu/my-apps) page. Then, enable the Dining API in the API section. An API key for the Dining API will be generated on the same page.

Create a duplicate of the `.env.example` file or rename it to `.env`. Paste the API key that you obtained from HUIT's API Portal into the indicated field.

### CS50 ID Authentication Setup
This project uses [CS50 ID](https://cs50.readthedocs.io/id.cs50.io/), an implementation of OpenID Connect built on Auth0 for authentication with HarvardKey. This is to ensure that users are only Harvard Affiliates and each user votes once per meal. (One vote per meal limit has yet to be implemented.) In order for this to work, one must register an app with CS50 ID at [id.cs50.io](https://id.cs50.io). To do so, you must log into CS50 ID either with HarvardKey or MIT Touchstone. Then, create an application by providing a description and redirection URL.

In order for this application to work, you must add the following redirection URLs:
```
http://[HOSTNAME]/callback
```

For example, if this application is hosted locally with a development Flask server, this would be:
```
http://127.0.0.1:5000/callback
```

Also, if HTTPS is enabled, the redirection URLs must be amended with the appropriate protocol.

Then, CS50 ID will provide you a Client Identifier, Client Secret, and OpenID Provider Metadata. These go into the `.env` file as described:
 - Client Identifier: `CLIENT_ID`
 - Client Secret: `CLIENT_SECRET`
 - OpenID Provider: `SERVER_METADATA_URL`

Now, your application will be able to use CS50 ID to provide identification services with HarvardKey.

## Usage
Once the virtual environment is created for this project, you can then start the Flask application in a development environment:

 - By activating the virtual environment and then running the Flask app as normal:
```bash
pipenv shell
flask run
```
 - Or running the app in the virtual environment with `pipenv run`:
```bash
pipenv run flask run
```
Then, a webserver will be started on your local computer at `localhost:5000` where you can access Munch. Optionally, you can also specify `--debug` to `flask run` if you want debug functionality like automatic updates when you edit files so you do not need to restart the flask server.

Alternatively, if you would like to run a production server, you can use the pre-installed `gunicorn` by substituting `flask run` with `gunicorn --workers=2 "app:app"`. Or, if you're feeling rebellious, you can use any Python WSGI server like `waitress`.

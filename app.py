import os
import sqlite3

from datetime import datetime
from sqlite3 import Error
from flask import Flask, jsonify, request
###
from flask_swagger_ui import get_swaggerui_blueprint

###

from Controller import Film
from Controller import Database

app = Flask(__name__)
app.register_blueprint(Film.route_blueprint)

###
SWAGGER_URL = '/doc'  # URL
API_URL = '/static/jsonSwagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={
		'app_name': "Film Documentation"
	},
	# oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
	#    'clientId': "your-client-id",
	#    'clientSecret': "your-client-secret-if-required",
	#    'realm': "your-realms",
	#    'appName': "your-app-name",
	#    'scopeSeparator': " ",
	#    'additionalQueryStringParams': {'test': "hello"}
	# }
)

app.register_blueprint(swaggerui_blueprint)


###

@app.route("/")
def index():
	return {"status": "API is running"}


@app.route("/fixture")
def setFixture():
	Database.fixture()
	return {"status": "ok"}


if __name__ == "__main__":
	if os.path.exists("bdd.db") is False:
		Database.fixture()
	app.run(debug=True)

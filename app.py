import os
import sqlite3

from datetime import datetime
from sqlite3 import Error
from flask import Flask, jsonify, request
###
from flask_swagger_ui import get_swaggerui_blueprint

###

app = Flask(__name__)

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

def fixture():
	bdd = create_connection(r"bdd.db")
	fd = open("schemaBdd.sql", 'r')
	sql_file_content = fd.read()
	fd.close()
	cursor = bdd.cursor()
	cursor.executescript(sql_file_content)
	bdd.commit()
	bdd.close()


def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	
	return conn


@app.route("/")
def index():
	return {"status": "API is running"}


@app.route("/fixture")
def setFixture():
	fixture()
	return {"status": "ok"}


# GET ALL FILMS
@app.route("/film/list", methods=["GET"])
def getListFilm():
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	try:
		cursor.execute("SELECT * FROM film")
		rows = cursor.fetchall()
		bdd.close()
		return jsonify({"status": 200}, rows)
	except sqlite3.Error:
		return jsonify({"status": 404})


# GET FILM (avec id)
@app.route("/film/<int:id>", methods=["GET"])
def getFilm(id):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	try:
		cursor.execute("SELECT * FROM film WHERE id = ?", (id,))
		rows = cursor.fetchall()
		bdd.close()
		return jsonify({"status": 200}, rows)
	except sqlite3.Error:
		return jsonify({"status": 404})


# CREATE FILM
# curl -X POST -H "Content-Type: application/json" -d '{"titre":"BBB", "description":"CCC", "date":"2023-01-01", "notation":"5"}' http://localhost:5000/film/create
# LANCEMENT TEST : 127.0.0.1:5000/film/create?titre=AAA&description=BBB&date=2000-10-01&notation=1
@app.route("/film/create", methods=["GET", "POST"])
def postFilm():
	global titre, description, dateFormat, notation
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	
	if request.method == "GET":
		# Récupe des arguments
		titre = request.args.get('titre')
		description = request.args.get('description')
		dateFormat = datetime.strptime(request.args.get('date'), "%Y-%m-%d")
		notation = request.args.get('notation')
	##
	elif request.method == "POST":
		# Récupe des arguments
		data = request.get_json()
		titre = data['titre']
		description = data['description']
		dateFormat = datetime.strptime(data['date'], "%Y-%m-%d")
		notation = data['notation']
	##
	
	try:
		sql = "INSERT INTO film (titre, description, dateParution, notation) VALUES (?, ?, ?, ?)"
		cursor.execute(sql, (titre, description, dateFormat, notation))
		bdd.commit()
		return {"status": "201", "id": cursor.lastrowid}
	except sqlite3.Error as error:
		return {"status": 422}


# DELETE FILM
@app.route("/film/delete/<int:id>", methods=["GET", "DELETE"])
def deleteFilm(id):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	try:
		cursor.execute("DELETE FROM film WHERE id = ?", (id,))
		bdd.commit()
		bdd.close()
		return {"status": "200", "id": id}
	except sqlite3.Error:
		return jsonify({"status": 422})


if __name__ == "__main__":
	if os.path.exists("bdd.db") is False:
		fixture()
	app.run(debug=True)
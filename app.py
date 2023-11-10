from datetime import datetime
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, request

app = Flask(__name__)


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
	cursor.execute("SELECT * FROM film")
	rows = cursor.fetchall()
	bdd.close()
	return jsonify({"status": 200}, rows)


# GET FILM (avec id)
@app.route("/film/<int:id>", methods=["GET"])
def getFilm(id):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	cursor.execute("SELECT * FROM film WHERE id = ?", (id,))
	rows = cursor.fetchall()
	bdd.close()
	return jsonify({"status": 200}, rows)


# CREATE FILM
# curl -X POST -H "Content-Type: application/json" -d '{"titre":"BBB", "description":"CCC", "date":"2023-01-01", "notation":"5"}' http://localhost:5000/film/create
# LANCEMENT TEST : 127.0.0.1:5000/film/create?titre=AAA&description=BBB&date=2000-10-01&notation=0
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
	
	sql = "INSERT INTO film (titre, description, dateParution, notation) VALUES (?, ?, ?, ?)"
	cursor.execute(sql, (titre, description, dateFormat, notation))
	bdd.commit()
	bdd.close()
	return {"status": "201"}


# DELETE FILM
@app.route("/film/delete/<int:id>", methods=["GET", "DELETE"])
def deleteFilm(id):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	cursor.execute("DELETE FROM film WHERE id = ?", (id,))
	bdd.commit()
	bdd.close()
	return {"status": "200"}


if __name__ == "__main__":
	app.run(debug=True)

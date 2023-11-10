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


@app.route("/film/list")
def getListFilm():
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	cursor.execute("SELECT * FROM film")
	rows = cursor.fetchall()
	bdd.close()
	return jsonify(rows)


@app.route("/film/<int:id>")
def getFilm(id):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	cursor.execute("SELECT * FROM film WHERE id = ?", (id,))
	rows = cursor.fetchall()
	username = request.args.get('username')
	bdd.close()
	return jsonify(rows)


# LANCEMENT TEST : 127.0.0.1:5000/film/create?titre=AAA&description=BBB&date=2000-10-01&notation=0
@app.route("/film/create", methods=["GET", "POST"])
def postFilm():
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()

	## Récupe des arguments
	titre = request.args.get('titre')
	description = request.args.get('description')
	dateFormat = datetime.strptime(request.args.get('date'), "%Y-%m-%d")
	notation = request.args.get('notation')
	##

	sql = "INSERT INTO film (titre, description, dateParution, notation) VALUES (?, ?, ?, ?)"
	cursor.execute(sql, (titre, description, dateFormat, notation))
	bdd.commit()

	bdd.close()
	return f"Film avec l'id {cursor.lastrowid} a été créé."


if __name__ == "__main__":
	fixture()
	app.run()

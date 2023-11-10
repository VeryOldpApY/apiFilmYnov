import sqlite3
from sqlite3 import Error
from flask import Flask

app = Flask(__name__)
bdd = None


def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		# Utilise le fichier pour créer la table film #
		with open('schemaBdd.sql') as f:
			conn.executescript(f.read())
		# #
		print(sqlite3.version)
	except Error as e:
		print(e)
	
	return conn


@app.route("/film/list")
def getListFilm():
	cursor = bdd.cursor()
	cursor.execute("SELECT * FROM film")
	rows = cursor.fetchall()
	return {rows}


@app.route("/film/{id}")
def getFilm():
	cursor = bdd.cursor()
	cursor.execute("SELECT * FROM film WHERE id = {id}")
	rows = cursor.fetchall()
	return {rows}


# @app.route("/film/put")
# def putFilm():
# 	cursor = bdd.cursor()
# 	cursor.execute("INSERT INTO film (id, titre, description, dateParution, notation) VALUES (2, 'AAA', 'BBB', to_date('05/11/2014', 'DD/MM/YYYY'), 0)")
# 	bdd.commit()

if __name__ == "__main__":
	bdd = create_connection(r"bdd.db")
	app.run()

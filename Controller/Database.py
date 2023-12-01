import sqlite3
import base64 ###############
from sqlite3 import Error

from flask import jsonify


def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	
	return conn


def fixture():
	bdd = create_connection(r"bdd.db")
	fd = open("schemaBdd.sql", 'r')
	sql_file_content = fd.read()
	fd.close()
	cursor = bdd.cursor()
	cursor.executescript(sql_file_content)

	bdd.commit()
	
	# img = iio.imread("../Resource/afficheInterstellar.jpg")
	with open("Resource/afficheInterstellar.jpg", "rb") as image_file:
		afficheEncoded = base64.b64encode(image_file.read())

	film_id = 1 # Interstellar

	sql = "INSERT INTO affiche (film_id, affiche) VALUES (?, ?)"
	data = request(sql, (film_id, afficheEncoded))

	bdd.commit()
	bdd.close()
	

def request(sql, params=None):
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	try:
		cursor.execute(sql, params)
		rows = cursor.fetchall()
		bdd.commit()
		bdd.close()
		return rows
	except sqlite3.Error:
		return None
	
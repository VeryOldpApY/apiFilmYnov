# GET ALL FILMS
import sqlite3
from datetime import datetime

from flask import jsonify, request, Blueprint

from Controller.Database import create_connection

route_blueprint = Blueprint('film', __name__)


@route_blueprint.route("/film/list", methods=["GET"])
def getListFilm():
	param = request.get_json()
	pageInit = param["pageInit"]
	pageLength = param["pageLength"]
	if pageInit is None:
		return jsonify({"status": 422, "message": "pageInit is null"})
	if pageLength is None:
		return jsonify({"status": 422, "message": "pageLength is null"})
	
	bdd = create_connection(r"bdd.db")
	cursor = bdd.cursor()
	try:
		cursor.execute("SELECT * FROM film LIMIT ?, ?", (pageInit, pageLength))
		rows = cursor.fetchall()
		bdd.close()
		return jsonify({"status": 200}, rows)
	except sqlite3.Error:
		return jsonify({"status": 422, "message": "SQL Error"})


# GET FILM (avec id)
@route_blueprint.route("/film/<int:id>", methods=["GET"])
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
@route_blueprint.route("/film/create", methods=["GET", "POST"])
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
@route_blueprint.route("/film/delete/<int:id>", methods=["GET", "DELETE"])
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

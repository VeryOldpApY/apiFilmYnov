# GET ALL FILMS
import uuid
from datetime import datetime

from flask import jsonify, request, Blueprint

from Controller import Database

route_blueprint = Blueprint('film', __name__)


# GET FILM (avec id)
@route_blueprint.route("/film", methods=["GET"])
def getFilm():
	param = request.get_json()
	uid = param["uid"]
	sql = "SELECT * FROM film WHERE uid = ?"
	data = Database.request(sql, (uid,))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	return jsonify({"status": 200}, data)


@route_blueprint.route("/film/list", methods=["GET"])
def getListFilm():
	param = request.get_json()
	page = param["page"] - 1
	if page is None:
		return jsonify({"status": 422, "message": "page is null"})
	
	sql = "SELECT * FROM film LIMIT ? OFFSET ?"
	data = Database.request(sql, ((page+1)*10, page*10))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	return jsonify({"status": 200}, data)


# CREATE FILM
# curl -X POST -H "Content-Type: application/json" -d '{"titre":"BBB", "description":"CCC", "date":"2023-01-01", "notation":"5"}' http://localhost:5000/film/create
# LANCEMENT TEST : 127.0.0.1:5000/film/create?titre=AAA&description=BBB&date=2000-10-01&notation=1
@route_blueprint.route("/film", methods=["POST"])
def postFilm():
	data = request.get_json()
	titre = data["titre"]
	description = data["description"]
	dateFormat = datetime.strptime(data["date"], "%Y-%m-%d")
	notation = data["notation"]
	uid = str(uuid.uuid4())
	
	sql = "INSERT INTO film (uid, titre, description, dateParution, notation) VALUES (?, ?, ?, ?, ?)"
	data = Database.request(sql, (str(uuid.uuid4()), titre, description, dateFormat, notation))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	return jsonify({"status": 200, "message": "Film created", "uid": uid})


# DELETE FILM
@route_blueprint.route("/film", methods=["DELETE"])
def deleteFilm():
	param = request.get_json()
	uid = param["uid"]
	
	sql = "DELETE FROM film WHERE uid = ?"
	data = Database.request(sql, (uid,))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	return jsonify({"status": 200, "message": "Film deleted"})

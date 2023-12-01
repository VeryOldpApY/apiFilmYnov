# GET ALL FILMS
import uuid
from datetime import datetime

from flask import jsonify, request, Blueprint

from Controller import Database

route_blueprint = Blueprint('film', __name__)


# GET film
@route_blueprint.route("/film", methods=["GET"])
def getFilm():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return jsonify({"status": 422, "message": "Parameters Error"})

	# SELECT film
	sql = "SELECT uid, titre, description, dateparution, notation FROM film WHERE uid = ?"
	dataFilm = Database.request(sql, (uid,))
	if dataFilm is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	
	# SELECT categorie
	sql = "SELECT c.uid, c.nom FROM categorie c, film_categorie fc WHERE fc.film_id = (SELECT id FROM film WHERE uid = ?) AND c.id = fc.categorie_id"
	dataCategorie = Database.request(sql, (uid,))
	if dataCategorie is None:
		return jsonify({"status": 422, "message": "SQL Error"})

	# ORGANISE pour l'affichage des categories dans un array dans le rendu json
	tupleCategorie = ()
	for i in dataCategorie:
		tupleCategorie += (i[1],)
	data = (*dataFilm[0], tupleCategorie)
	
	return jsonify({"status": 200}, data)


# LIST films
@route_blueprint.route("/film/list", methods=["GET"])
def getListFilm():
	param = request.get_json()
	try:
		page = int(param.get("page", 1)) - 1
		if page is None or page < 0:
			return jsonify({"status": 422, "message": "Parameters Error"})
	except ValueError:
		return jsonify({"status": 422, "message": "Parameters Error"})
	
	# SELECT film
	sql = "SELECT uid, titre, description, dateparution, notation FROM film LIMIT ? OFFSET ?"
	dataFilm = Database.request(sql, ((page+1)*10, page*10))
	if dataFilm is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	
	data = []	
	for i in dataFilm:
		# SELECT categorie
		sql = "SELECT c.uid, c.nom FROM categorie c, film_categorie fc WHERE fc.film_id = (SELECT id FROM film WHERE uid = ?) AND c.id = fc.categorie_id"
		dataCategorie = Database.request(sql, (i[0],)) # iud
		if dataCategorie is None:
			return jsonify({"status": 422, "message": "SQL Error"})

		# ORGANISE pour l'affichage des categories dans un array dans le rendu json
		tupleCategorie = ()
		for y in dataCategorie:
			tupleCategorie += (y[1],)
		data.append( (*i, tupleCategorie) )

	return jsonify({"status": 200}, data)


# CREATE film
@route_blueprint.route("/film", methods=["POST"])
def postFilm():
	data = request.get_json()
	titre = data["titre"]
	description = data["description"]
	dateFormat = datetime.strptime(data["date"], "%Y-%m-%d")
	notation = int(data["notation"])
	categorie = data["categorie"]
	uid = str(uuid.uuid4())
	data = None
	while data is not None:
		uid = str(uuid.uuid4())
		data = Database.request("SELECT uid FROM film WHERE uid = ?", (uid,))
		
	if titre is None or description is None or dateFormat is None or notation is None:
		return jsonify({"status": 422, "message": "Parameters Error"})

	# CHECK SI TITRE FILM EXISTE DEJA
	sql = "SELECT uid FROM film WHERE titre = ?"
	data = Database.request(sql, (titre,))
	if data:
		return jsonify({"status": 422, "message": "Parameters Error, un film avec le titre '"+titre+"' existe déjà"}, data)

	# RECUP LES UID DES CATEGORIES + CHECK SI ELLES EXISTENT
	listeCategorieId = []
	for i in categorie:
		sql = "SELECT id FROM categorie WHERE nom = ?"
		data = Database.request(sql, (i,))
		if data is None:
			return jsonify({"status": 422, "message": "Parameters Error, la categorie "+i+" n'existe pas"})
		listeCategorieId.append(data)

	# INSERT FILM
	sql = "INSERT INTO film (uid, titre, description, dateParution, notation) VALUES (?, ?, ?, ?, ?)"
	data = Database.request(sql, (str(uuid.uuid4()), titre, description, dateFormat, notation))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	
	# RECUP ID DE FILM
	sql = "SELECT id FROM film WHERE titre = ?"
	filmId = Database.request(sql, (titre,))

	# INSERT film_categorie UNIQUEMENT SI IL Y A DES CATEGORIES A AJOUTER
	if len(listeCategorieId) != 0:
		for categorieId in listeCategorieId:
			sql = "INSERT INTO film_categorie (film_id, categorie_id) VALUES (?, ?)"
			data = Database.request(sql, (filmId, categorieId))
			if data is None:
				return jsonify({"status": 422, "message": "SQL Error"})
	
	return jsonify({"status": 200, "message": "Film created", "uid": uid})


# DELETE film
@route_blueprint.route("/film", methods=["DELETE"])
def deleteFilm():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return jsonify({"status": 422, "message": "Parameters Error"})
	
	sql = "DELETE FROM film WHERE uid = ?"
	data = Database.request(sql, (uid,))
	if data is None:
		return jsonify({"status": 422, "message": "SQL Error"})
	return jsonify({"status": 200, "message": "Film deleted"})


# ADD/REMOVE film's categories
@route_blueprint.route("/film/categorie", methods=["PUT"])
def Film_Categeorie():
	param = request.get_json()
	filmUid = param["filmUid"]
	addCategorie = param["addCategorie"]
	removeCategorie = param["removeCategorie"]

	# CHECK SI LES CATEGORIES EXISTENT
	for i in addCategorie:
		if i != "":
			sql = "SELECT id FROM categorie WHERE nom = ?"
			data = Database.request(sql, (i,))
			if data == []:
				return jsonify({"status": 422, "message": "Parameters Error, la categorie "+i+" n'existe pas"})
	for i in removeCategorie:
		if i != "":
			sql = "SELECT id FROM categorie WHERE nom = ?"
			data = Database.request(sql, (i,))
			if data == []:
				return jsonify({"status": 422, "message": "Parameters Error, la categorie "+i+" n'existe pas"})

	# INSERT film_categorie
	for categorieName in addCategorie:
		sql = "INSERT INTO film_categorie (film_id, categorie_id) SELECT (SELECT id FROM film WHERE uid = ?), id FROM categorie WHERE nom = ?;"
		data = Database.request(sql, (filmUid, categorieName))
		if data is None:
			return jsonify({"status": 422, "message": "SQL Error"})

	# DELETE film_categorie
	for categorieName in removeCategorie:
		sql = "DELETE FROM film_categorie WHERE film_id = (SELECT id FROM film WHERE uid = ?) AND categorie_id = (SELECT id FROM categorie WHERE nom = ?)"
		data = Database.request(sql, (filmUid, categorieName))
		if data is None:
			return jsonify({"status": 422, "message": "SQL Error"})	
	
	return jsonify({"status": 200, "message": "Film's categories updated"})
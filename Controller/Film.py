# GET ALL FILMS
import uuid
import base64
from datetime import datetime

from flask import jsonify, request, Blueprint

from Controller import Database
from Util.API import returnAPIFormat

route_blueprint = Blueprint('film', __name__)


# GET film
@route_blueprint.route("/film", methods=["GET"])
def getFilm():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	# SELECT film
	sql = "SELECT uid, titre, description, dateparution, notation FROM film WHERE uid = ?"
	dataFilm = Database.request(sql, (uid,))
	if dataFilm is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	data = {
		"uid": dataFilm[0][0],
		"titre": dataFilm[0][1],
		"description": dataFilm[0][2],
		"dateParution": dataFilm[0][3],
		"notation": dataFilm[0][4],
		"categorie": []
	}
	
	# SELECT categorie
	sql = "SELECT c.uid, c.nom FROM categorie c, film_categorie fc WHERE fc.film_id = (SELECT id FROM film WHERE uid = ?) AND c.id = fc.categorie_id"
	dataCategorie = Database.request(sql, (uid,))
	if dataCategorie is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	for i in dataCategorie:
		data["categorie"].append(i[1])
		
	return returnAPIFormat(data=data, link=request.path, method=request.method)


# LIST films
@route_blueprint.route("/film/list", methods=["GET"])
def getListFilm():
	param = request.get_json()
	try:
		page = int(param.get("page", 1)) - 1
		if page is None or page < 0:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	except ValueError:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	# SELECT film
	sql = "SELECT uid, titre, description, dateparution, notation FROM film LIMIT ? OFFSET ?"
	dataFilm = Database.request(sql, ((page + 1) * 10, page * 10))
	if dataFilm is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	data = []
	for film in dataFilm:
		sql = "SELECT c.uid, c.nom FROM categorie c, film_categorie fc WHERE fc.film_id = (SELECT id FROM film WHERE uid = ?) AND c.id = fc.categorie_id"
		dataCategorie = Database.request(sql, (film[0],))  # iud
		if dataCategorie is None:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
		
		data.append({
			"uid": film[0],
			"titre": film[1],
			"description": film[2],
			"dateParution": film[3],
			"notation": film[4],
			"categorie": []
		})
		for categorie in dataCategorie:
			data[-1]["categorie"].append(categorie[1])
	
	return returnAPIFormat(data=data, link=request.path, method=request.method)


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
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	# CHECK SI TITRE FILM EXISTE DEJA
	sql = "SELECT uid FROM film WHERE titre = ?"
	data = Database.request(sql, (titre,))
	if data:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error, le titre du film existe déjà")
	
	# RECUP LES UID DES CATEGORIES + CHECK SI ELLES EXISTENT
	listeCategorieId = []
	for i in categorie:
		sql = "SELECT id FROM categorie WHERE nom = ?"
		data = Database.request(sql, (i,))
		if data is None:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error, la categorie n'existe pas")
		listeCategorieId.append(data)
	
	# INSERT FILM
	sql = "INSERT INTO film (uid, titre, description, dateParution, notation) VALUES (?, ?, ?, ?, ?)"
	Database.request(sql, (str(uuid.uuid4()), titre, description, dateFormat, notation))
	
	# RECUP ID DE FILM
	sql = "SELECT id FROM film WHERE titre = ?"
	filmId = Database.request(sql, (titre,))
	if filmId is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	# INSERT film_categorie UNIQUEMENT SI IL Y A DES CATEGORIES A AJOUTER
	if len(listeCategorieId) != 0:
		for categorieId in listeCategorieId:
			sql = "INSERT INTO film_categorie (film_id, categorie_id) VALUES (?, ?)"
			Database.request(sql, (filmId, categorieId))

	data = {
		"uid": uid
	}
	
	return returnAPIFormat(data=data, link=request.path, method=request.method, status=200, message="Film created")


# DELETE film
@route_blueprint.route("/film", methods=["DELETE"])
def deleteFilm():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	sql = "DELETE FROM film WHERE uid = ?"
	data = Database.request(sql, (uid,))
	if data is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	return returnAPIFormat(data=None, link=request.path, method=request.method, status=200, message="Film deleted")


# ADD/REMOVE film's categories
@route_blueprint.route("/film/categorie", methods=["PUT"])
def Film_Categeorie():
	param = request.get_json()
	filmUid = param["filmUid"]
	addCategorie = param["addCategorie"]
	removeCategorie = param["removeCategorie"]
	if filmUid is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	# CHECK SI LES CATEGORIES EXISTENT
	for i in addCategorie:
		if i != "":
			sql = "SELECT id FROM categorie WHERE nom = ?"
			data = Database.request(sql, (i,))
			if not data:
				return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error, la categorie n'existe pas")
	for i in removeCategorie:
		if i != "":
			sql = "SELECT id FROM categorie WHERE nom = ?"
			data = Database.request(sql, (i,))
			if not data:
				return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error, la categorie n'existe pas")
	
	# INSERT film_categorie
	for categorieName in addCategorie:
		sql = "INSERT INTO film_categorie (film_id, categorie_id) SELECT (SELECT id FROM film WHERE uid = ?), id FROM categorie WHERE nom = ?;"
		data = Database.request(sql, (filmUid, categorieName))
		if data is None:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	# DELETE film_categorie
	for categorieName in removeCategorie:
		sql = "DELETE FROM film_categorie WHERE film_id = (SELECT id FROM film WHERE uid = ?) AND categorie_id = (SELECT id FROM categorie WHERE nom = ?)"
		data = Database.request(sql, (filmUid, categorieName))
		if data is None:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	return returnAPIFormat(data=None, link=request.path, method=request.method, status=200, message="Categories updated")


# Créer JPG de l'affiche du film indiqué
@route_blueprint.route("/film/affiche/createJPG", methods=["GET"])
def Film_Affiche_CreateJPG():
	param = request.get_json()
	filmTitre = param["filmTitre"]
	if filmTitre is None:
		return jsonify({"status": 422, "message": "Parameters Error"})
	
	sql = "SELECT a.affiche, f.titre FROM film f, affiche a WHERE f.titre = ? and a.film_id = f.id"
	dataTest = Database.request(sql, (filmTitre,))
	if dataTest is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	with open("FilesOut/Affiche de " + dataTest[0][1] + ".jpg", "wb") as file:
		file.write(base64.b64decode(dataTest[0][0]))
	
	return returnAPIFormat(data=None, link=request.path, method=request.method, status=200, message="Affiche created")

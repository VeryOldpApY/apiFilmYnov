import uuid
from datetime import datetime

from flask import jsonify, request, Blueprint

from Controller import Database
from Util.API import returnAPIFormat

route_blueprint = Blueprint('categorie', __name__)


# GET categorie
@route_blueprint.route("/categorie", methods=["GET"])
def getCategorie():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	sql = "SELECT uid, nom FROM categorie WHERE uid = ?"
	dataCategorie = Database.request(sql, (uid,))
	if dataCategorie is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	data = {
		"uid": dataCategorie[0][0],
		"nom": dataCategorie[0][1]
	}

	return returnAPIFormat(data=data, link=request.path, method=request.method)


# GET categorie's film
@route_blueprint.route("/categorie/film", methods=["GET"])
def getCategorieFilm():
	param = request.get_json()
	nom = param["nom"]
	if nom is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	sql = """SELECT f.uid, f.titre, f.description, f.dateparution, f.notation
		FROM film_categorie fc, film f WHERE fc.categorie_id = (SELECT id FROM categorie WHERE nom = ?) AND f.id = fc.film_id"""
	dataCategorie = Database.request(sql, (nom,))
	if dataCategorie is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	data = []

	for categorie in dataCategorie:
		data.append({
		"uid": categorie[0],
		"titre": categorie[1],
		"description": categorie[2],
		"dateparution": categorie[3],
		"notation": categorie[4]
		})
	
	return returnAPIFormat(data=data, link=request.path, method=request.method)


# LIST categories
@route_blueprint.route("/categorie/list", methods=["GET"])
def getListCategorie():
	param = request.get_json()
	try:
		page = int(param.get("page", 1)) - 1
		if page is None or page < 0:
			return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	except ValueError:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	sql = "SELECT uid, nom FROM categorie LIMIT ? OFFSET ?"
	dataCategorie = Database.request(sql, ((page+1)*10, page*10))
	if dataCategorie is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	data = []
	for categorie in dataCategorie:
		data.append({
			"uid": categorie[0],
			"nom": categorie[1]
		})

	return returnAPIFormat(data=data, link=request.path, method=request.method)

# CREATE categorie
@route_blueprint.route("/categorie", methods=["POST"])
def postCategorie():
	data = request.get_json()
	nom = data["nom"]
	uid = str(uuid.uuid4())
	if nom is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")
	
	sql = "INSERT INTO categorie (uid, nom) VALUES (?, ?)"
	dataCategorie = Database.request(sql, (str(uid), nom))
	if dataCategorie is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")

	data = {
		"uid": uid
	}

	return returnAPIFormat(data=data, link=request.path, method=request.method)

# DELETE categorie
@route_blueprint.route("/categorie", methods=["DELETE"])
def deleteCategorie():
	param = request.get_json()
	uid = param["uid"]
	if uid is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="Parameters Error")

	# DELETE film_categorie (enlève la catégorie à tous les films)
	sql = "DELETE FROM film_categorie WHERE categorie_id = (SELECT id FROM categorie WHERE uid = ?)"
	data = Database.request(sql, (uid,))
	if data is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")

	# DELETE la categorie
	sql = "DELETE FROM categorie WHERE uid = ?"
	data = Database.request(sql, (uid,))
	if data is None:
		return returnAPIFormat(data=None, link=request.path, method=request.method, status=422, message="SQL Error")
	
	return returnAPIFormat(data=None, link=request.path, method=request.method, status=200, message="categorie deleted")
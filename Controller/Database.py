import sqlite3
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


# def request(sql, params=None, type):
# 	bdd = create_connection(r"bdd.db")
# 	cursor = bdd.cursor()
# 	try:
# 		if type == "SELECT":
# 			cursor.execute(sql, params)
# 			rows = cursor.fetchall()
# 			bdd.close()
# 			return rows
# 		elif type == "INSERT":
# 			cursor.execute(sql, params)
# 			bdd.commit()
# 			last_row_id = cursor.lastrowid
# 			bdd.close()
# 			return last_row_id
# 		elif type == "UPDATE":
# 			cursor.execute(sql, params)
# 			bdd.commit()
# 			bdd.close()
# 			return True
# 		elif type == "DELETE":
# 			cursor.execute(sql, params)
# 			bdd.commit()
# 			bdd.close()
# 			return True
# 	except sqlite3.Error:
# 		return None


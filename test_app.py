import requests


url = "http://localhost:5000"
headers = {'Content-Type': 'application/json'}


def test_index():
	payload = dict("")
	assert requests.get(url+"/", data=payload, headers=headers).json() == {"status": "API is running"}


def test_fixture():
	payload = dict()
	assert requests.get(url+"/fixture", data=payload, headers=headers).json() == {"status": "ok"}
	
	

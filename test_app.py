import app

url = "http://localhost:5000"
headers = {'Content-Type': 'application/json'}


def test_index():
	assert app.index() == {"status": "API is running"}


def test_fixture():
	assert app.setFixture() == {"status": "ok"}

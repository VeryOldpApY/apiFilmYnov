import os
import zipfile

import requests

api_url = f"https://api.github.com/repos/VeryOldpApY/apiFilmYnov/releases/latest"

# Faire une requête HTTP GET à l'API GitHub
response = requests.get(api_url)
response.raise_for_status()  # Gérer les erreurs HTTP

# Obtenir les données JSON de la réponse
release_info = response.json()

# Obtenir le lien de téléchargement de l'archive
download_url = release_info["zipball_url"]

# Télécharger l'archive
archive = requests.get(download_url)

# Enregistrer l'archive dans un fichier
with open("archive.zip", "wb") as file:
	file.write(archive.content)

# Extraire l'archive
with zipfile.ZipFile("archive.zip", "r") as zip_ref:
	zip_ref.extractall("./test")

# Supprimer l'archive
os.remove("archive.zip")
os.system("cd test && python3 -m pip install -r requirements.txt")

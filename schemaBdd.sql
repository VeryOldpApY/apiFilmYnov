DROP TABLE IF EXISTS film;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS film_categorie;

CREATE TABLE film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    titre TEXT NOT NULL UNIQUE,
    description TEXT,
    dateParution DATE,
    notation INT
);

CREATE TABLE categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    nom TEXT NOT NULL UNIQUE
);

CREATE TABLE film_categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    categorie_id INTEGER NOT NULL,
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (categorie_id) REFERENCES categorie(id)
);

-- LES INSERT
INSERT INTO film (uid, titre, description, dateParution, notation)
VALUES ('uid', 'Interstellar', 'Super film de Nolan', '2014-11-05', 5),
('uid1', 'titre1', 'description1', '2020-01-01', 1),
('uid2', 'titre2', 'description2', '2020-01-01', 1),
('uid3', 'titre3', 'description3', '2020-01-01', 1),
('uid4', 'titre4', 'description4', '2020-01-01', 1),
('uid5', 'titre5', 'description5', '2020-01-01', 1),
('uid6', 'titre6', 'description6', '2020-01-01', 1),
('uid7', 'titre7', 'description7', '2020-01-01', 1),
('uid8', 'titre8', 'description8', '2020-01-01', 1),
('uid9', 'titre9', 'description9', '2020-01-01', 1),
('uid10', 'titre10', 'description10', '2020-01-01', 1),
('uid11', 'titre11', 'description11', '2020-01-01', 1),
('uid12', 'titre12', 'description12', '2020-01-01', 1),
('uid13', 'titre13', 'description13', '2020-01-01', 1),
('uid14', 'titre14', 'description14', '2020-01-01', 1)
;

INSERT INTO categorie (uid, nom) VALUES ('uid1', 'Science Fiction'), ('uid2', 'Drame'), ('uid3', 'Christopher Nolan');

INSERT INTO film_categorie (film_id, categorie_id) VALUES (1, 1), (1, 2), (1, 3);
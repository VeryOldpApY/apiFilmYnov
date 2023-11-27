DROP TABLE IF EXISTS film;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS film_categorie;

CREATE TABLE film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    titre TEXT NOT NULL,
    description TEXT,
    dateParution DATE,
    notation INT
);

CREATE TABLE categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    nom TEXT NOT NULL
);

CREATE TABLE film_categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    categorie_id INTEGER NOT NULL,
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (categorie_id) REFERENCES categorie(id)
);



-- LES INSERT
INSERT INTO film (id, titre, description, dateParution, notation)
VALUES (1, 'Interstellar', 'Super film de Nolan', '2014-11-05', 5);

INSERT INTO categorie (id, nom)
VALUES (1, 'Science Fiction'), (2, 'Drame'), (3, 'Christopher Nolan')
;

INSERT INTO film_categorie (film_id, categorie_id)
VALUES (1, 1), (1, 2), (1, 3);
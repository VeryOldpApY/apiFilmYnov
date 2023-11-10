DROP TABLE IF EXISTS film;

CREATE TABLE film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    dateParution DATE,
    notation INT
);

INSERT INTO film (titre, description, dateParution, notation)
VALUES ('Interstellar', 'Super film de Nolan', '2014-11-05', 5);
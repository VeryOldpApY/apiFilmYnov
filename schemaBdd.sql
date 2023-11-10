DROP TABLE IF EXISTS posts;

CREATE TABLE film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    dateParution DATE,
    notation REAL
);

INSERT INTO film (titre, description, dateParution, notation)
VALUES ('Interstellar', 'Super film de Nolan', to_date('05/11/2014', 'DD/MM/YYYY'), 5);
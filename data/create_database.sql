-- to je datoteka za ustvarjanje baze podatkov in tabel

CREATE TABLE IF NOT EXISTS oseba
( 
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL, 
    priimek TEXT NOT NULL,
    elektronski_naslov TEXT NOT NULL UNIQUE,
    uporabnisko_ime TEXT NOT NULL UNIQUE,
    geslo TEXT NOT NULL
);
-- komentar

CREATE TABLE IF NOT EXISTS sladica
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    cas_priprave INTEGER NOT NULL,
    -- tezavnost INTEGER napisi requirements, 
    postopek TEXT NOT NULL,
    kratek_opis TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS tezavnost
(
    id INTEGER PRIMARY KEY,
    tezavnost TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS kategorija
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS sestavina
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL
)


CREATE TABLE IF NOT EXISTS pripomocki
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL
)

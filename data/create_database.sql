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

CREATE TABLE IF NOT EXISTS tezavnost
(
    id INTEGER PRIMARY KEY,
    tezavnost TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kategorija
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sladica
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    cas_priprave INTEGER NOT NULL,
    -- tezavnost INTEGER napisi requirements, 
    postopek TEXT NOT NULL,
    kratek_opis TEXT NOT NULL,
    avtor INTEGER NOT NULL REFERENCES oseba(id),
    tezavnost INTEGER NOT NULL REFERENCES tezavnost(id),
    kategorija INTEGER NOT NULL REFERENCES kategorija(id)
);
--komentar 2



-- drop table if exists sestavina cascade;

CREATE TABLE IF NOT EXISTS sestavina
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    enota TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS pripomocek
(
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vsebuje
(
    sladica INTEGER NOT NULL REFERENCES sladica(id),
    sestavina INTEGER NOT NULL REFERENCES sestavina(id),
    kolicina_sestavine TEXT NOT NULL,
    PRIMARY KEY(sladica, sestavina)
);

CREATE TABLE IF NOT EXISTS potrebujes
(
    sladica INTEGER NOT NULL REFERENCES sladica(id),
    pripomocek INTEGER NOT NULL REFERENCES pripomocek(id),
    PRIMARY KEY(sladica, pripomocek)
);

CREATE TABLE IF NOT EXISTS priljubljeno
(
    sladica INTEGER NOT NULL REFERENCES sladica(id),
    oseba INTEGER NOT NULL REFERENCES oseba(id),
    PRIMARY KEY(sladica, oseba)
);


-- CREATE TABLE IF NOT EXISTS public.uporabniki
-- (
--     username text PRIMARY KEY,
--     role text not null,
--     password text not null,
--     last_login timestamp
-- );
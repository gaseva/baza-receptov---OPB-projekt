-- dovolimo povezavo in uporabo scheme public javnosti
GRANT CONNECT ON DATABASE sem2026_anabar TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;

-- dovolimo vse nekemu konkretnemu uporabniku soclan (WITH GRANT option, dovoli uporabniku dovoljevati pravice)
GRANT ALL ON DATABASE sem2026_anabar TO evagas WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO evagas WITH GRANT OPTION;

-- po ustvarjanju tabel
GRANT ALL ON ALL TABLES IN SCHEMA public TO evagas WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO evagas WITH GRANT OPTION;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;

-- dodatne pravice za uporabo aplikacije
GRANT INSERT ON oseba, sladica, sestavina, pripomocek TO javnost;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO javnost;
GRANT INSERT ON vsebuje, potrebujes, priljubljeno TO javnost;
GRANT DELETE ON priljubljeno, potrebujes, vsebuje, sladica TO javnost;
GRANT UPDATE ON vsebuje TO javnost;

-- privzete pravice za OBJEKTE, ki jih boš ustvaril v prihodnje
    
-- nove tabele/pogledi v shemi public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO evagas WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO javnost;

-- nove sekvence v shemi public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO evagas WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO javnost;


INSERT INTO oseba
    (ime, priimek, elektronski_naslov, uporabnisko_ime, geslo_hash)
VALUES
('Maja', 'Kovač', 'maja.kovac@example.com', 'maja3', '$2b$12$wdS2nzjRe89nBjopl.ZxHOztQk7wFmikP3ZtPQBjkptygAN/lMOSC'),
('Luka', 'Zupan', 'luka.zupan@example.com', 'luka7', '$2b$12$COC4ZqgxW6jF0s10lB.KNuKOtt7TLrDfJnT7pzkQjNNFxlBMaYErS'),
('Nina', 'Kralj', 'nina.kralj@example.com', 'nina11', '$2b$12$6vfD3VpuaIdkxnueJXhxheR8Uyqf93Hzq1CnZ4r.g9EQY6LP3eHCO'),
('Ana', 'Novak', 'ana.novak@example.com', 'ana12', '$2b$12$myopO3.Kl8IfT5il4zMlV.YNGIZUdQK3TUjYDMSRi6X07//bBiepG'),
('Eva', 'Mlakar', 'eva.mlakar@example.com', 'eva16', '$2b$12$A33a8FgaJQ7PIJbJtbqDAOQSqNxezkx5PemACP.sWQLPU3WifXk82'),
('Sara', 'Kos', 'sara.kos@example.com', 'sara23', '$2b$12$m9b33NB1WFb6iZGDxLEwN.dc47KvZuw3iO/esNSuAqNNZaVqkCB.K'),
('Miha', 'Vidmar', 'miha.vidmar@example.com', 'miha28', '$2b$12$SzQ1SAnvd0KztkHQZ2T/rOtrRQjXoshekIsfug4u.zqMN6XlakwRe'),
('Tina', 'Horvat', 'tina.horvat@example.com', 'tina34', '$2b$12$6YqDvnuu3UxyVvVKT9GfneaDj9fmNMfpW7AbIDZ2sTc42QPIvHE0e'),
('Jan', 'Rozman', 'jan.rozman@example.com', 'jan39', '$2b$12$60c5JqoXhCjvix2/Vbrne..ylYBKvCGozF/dLzAdedsNdE6nrvhNW'),
('Neža', 'Potočnik', 'neza.potocnik@example.com', 'neza45', '$2b$12$32/EcCrdwy9dvmzyQHl1xuS9RP5QSE1zwRKRKowNPPxxYDySMx3xe'),
('Urša', 'Golob', 'ursa.golob@example.com', 'ursa49', '$2b$12$byDZMz3nF3AvBZQYOKu9cuk1fCHQ7tr84FCXMZnxOiRikpxO7FyuC'),
('Rok', 'Turk', 'rok.turk@example.com', 'rok52', '$2b$12$80.KLjTiUs2itJ1Nkqa1lOOzUmUZx.dAGmg3Sfg5q6erwPtAQL8eO'),
('Klara', 'Bizjak', 'klara.bizjak@example.com', 'klara58', '$2b$12$OuYY.ZECKuxHiKR64zSz4OTy6DArR.KUbRkxoN22RmOkzGkP9h3sG'),
('Žan', 'Božič', 'zan.bozic@example.com', 'zan62', '$2b$12$fWcYEzHPKoVVNEEFIYdi2OcW41q.eeNgy9kt764E94R49hX4/vcey'),
('Ema', 'Kavčič', 'ema.kavcic@example.com', 'ema67', '$2b$12$jTBNMihuA5nd7upI1RjINuG2TPjvL6hI9v8BZtOpG1YiittIhdHf2'),
('Jakob', 'Zajc', 'jakob.zajc@example.com', 'jakob76', '$2b$12$dVXFL48wBYsSBXl/FgsP/uhl.o71JkCwBiZrLjIUxnvM16SGlHf12'),
('Lana', 'Petek', 'lana.petek@example.com', 'lana84', '$2b$12$ut6LW6vUyHP5S7D1Qyv60up.90Tjcz.4mTz7EjZy4C/RBlNP1uNGG'),
('Tjaša', 'Koren', 'tjasa.koren@example.com', 'tjasa88', '$2b$12$WFSx5.beHAHQIYEHPGBVb./nYrcRU03G4J.eN7/.K0KgFn/qSZVUe'),
('Vid', 'Kastelic', 'vid.kastelic@example.com', 'vid91', '$2b$12$C6/EGi1UqpT2sg1qUWtO0eHgnsX3bwq3xOWUsHYSTjBicndURbQJK'),
('Ajda', 'Kranjc', 'ajda.kranjc@example.com', 'ajda95', '$2b$12$zyBM.y1A7yv1lhhJM/ihS.bgjQ4VOUnEXADRp9udYBtcYSYB5sRxy')
ON CONFLICT (id) DO UPDATE SET
    ime = EXCLUDED.ime,
    priimek = EXCLUDED.priimek,
    elektronski_naslov = EXCLUDED.elektronski_naslov,
    uporabnisko_ime = EXCLUDED.uporabnisko_ime,
    geslo_hash = EXCLUDED.geslo_hash,
    rola = EXCLUDED.rola;


select * from oseba;


INSERT INTO tezavnost (id, ime)
VALUES
(1, 'enostavno'),
(2, 'srednje'),
(3, 'zahtevno')
ON CONFLICT (id) DO UPDATE SET ime = EXCLUDED.ime;

-- select * from tezavnost;


INSERT INTO kategorija (id, ime)
VALUES
(1, 'torte'),
(2, 'piškoti'),
(3, 'mafini'),
(4, 'drobno pecivo'),
(5, 'sladoled'),
(6, 'kreme'),
(7, 'napitki'),
(8, 'pite'),
(9, 'zavitki'),
(10, 'ostalo')
ON CONFLICT (id) DO UPDATE SET ime = EXCLUDED.ime;

-- select * from kategorija;

INSERT INTO sladica
(ime, cas_priprave, postopek, kratek_opis, avtor, tezavnost, kategorija)
VALUES

(
'Čokoladna torta',
90,
'Najprej pečico segrejemo na 180 °C. Čokolado in maslo stopimo nad paro ter pustimo, da se nekoliko ohladi. V večji posodi stepemo jajca in sladkor, dokler masa ne postane svetla in puhasta. Dodamo stopljeno čokolado, moko in pecilni prašek ter nežno premešamo. Maso vlijemo v namaščen tortni model in pečemo približno 45 minut. Medtem pripravimo čokoladno kremo iz sladke smetane in čokolade. Ohlajen biskvit prerežemo na dve plasti, premažemo s kremo in torto okrasimo s čokoladnimi ostružki.',
'Bogata čokoladna torta z mehkim biskvitom in kremasto čokoladno sredico.',
1,
3,
1
),

(
'Vanilijevi mafini',
45,
'V eni posodi zmešamo moko, pecilni prašek in sladkor. V drugi posodi stepemo jajca, mleko in stopljeno maslo. Mokre sestavine postopoma primešamo suhim in dodamo vanilijev ekstrakt. Maso razdelimo v modelčke za mafine do približno dveh tretjin višine. Mafine pečemo 20–25 minut, da postanejo zlato rjavi. Pred serviranjem jih ohladimo in po želji posujemo s sladkorjem v prahu.',
'Mehki in rahli mafini z nežnim okusom vanilije.',
2,
1,
3
),

(
'Jagodni cheesecake',
135,
'Piškote zdrobimo v drobne drobtine in jih zmešamo s stopljenim maslom. Zmes vtisnemo na dno tortnega modela. Kremni sir stepemo s sladkorjem, dodamo jajca in vanilijo. Kremo vlijemo na podlago in pečemo približno eno uro pri nižji temperaturi. Ko se torta ohladi, jo premažemo z jagodnim prelivom iz svežih jagod in sladkorja ter postavimo v hladilnik za vsaj dve uri.',
'Osvežilna torta z bogato sirno kremo in sladkimi jagodami.',
7,
2,
1
),

(
'Masleni piškoti',
60,
'Iz moke, masla, sladkorja in jajca zgnetemo gladko testo. Testo zavijemo v folijo in ga pustimo počivati v hladilniku približno 30 minut. Nato ga razvaljamo na pomokani površini in z modelčki izrežemo različne oblike. Piškote pečemo 10–12 minut pri 180 °C, dokler rahlo ne porjavijo. Ohlajene lahko okrasimo s čokolado ali sladkorno glazuro.',
'Klasični domači piškoti, ki se odlično podajo k čaju ali kavi.',
9,
1,
2
),

(
'Čokoladni mousse',
45,
'Temno čokolado stopimo nad paro in pustimo, da se nekoliko ohladi. Sladko smetano stepemo do mehkih vrhov. Ločeno stepemo beljake s sladkorjem. V stopljeno čokolado najprej vmešamo rumenjake, nato stepeno smetano in na koncu še beljake. Mousse razdelimo v kozarčke in ga hladimo vsaj dve uri. Pred serviranjem ga okrasimo z naribano čokolado ali sadjem.',
'Lahka in puhasta čokoladna krema intenzivnega okusa.',
12,
2,
6
),

(
'Sadna pita',
75,
'Iz moke, masla in sladkorja pripravimo krhko testo. Testo razvaljamo in položimo v model za pito. Podlago pečemo približno 15 minut. Nato dodamo vanilijevo kremo in sveže sadje, kot so jagode, borovnice in kivi. Pito pečemo še dodatnih 20 minut in jo pred serviranjem dobro ohladimo.',
'Hrustljava pita s svežim sadjem in nežno vanilijevo kremo.',
20,
2,
8
),

(
'Tiramisu',
60,
'Skuhamo močno kavo in jo ohladimo. Rumenjake stepemo s sladkorjem, nato dodamo mascarpone. Beljake posebej stepemo v trd sneg in jih nežno vmešamo v kremo. Baby piškote pomočimo v kavo in jih zlagamo v pekač. Čez nanesemo plast kreme in postopek ponovimo. Tiramisu hladimo čez noč ter ga pred serviranjem posujemo s kakavom.',
'Tradicionalna italijanska sladica s kavno aromo in mascarponejem.',
14,
1,
6
),

(
'Kokosove kroglice',
30,
'Piškote zdrobimo in jih zmešamo s kakavom, kokosom in kondenziranim mlekom. Maso dobro pregnetemo in oblikujemo majhne kroglice. Vsako kroglico povaljamo v kokosovi moki. Sladico postavimo v hladilnik za vsaj 30 minut, da se strdi.',
'Hitre kokosove sladice brez peke.',
16,
1,
4
),

(
'Browniji',
45,
'Čokolado in maslo stopimo nad paro. Dodamo sladkor in eno po eno umešamo jajca. Nato primešamo moko in ščepec soli. Maso vlijemo v manjši pekač in pečemo približno 25 minut. Browniji morajo ostati rahlo mehki v sredini. Pred rezanjem jih popolnoma ohladimo.',
'Mehki čokoladni browniji z bogatim okusom kakava.',
16,
1,
4
),

(
'Limonina pita',
75,
'Najprej pripravimo krhko testo in ga spečemo do zlato rumene barve. Medtem v kozici segrejemo limonin sok, sladkor in maslo. Dodamo stepena jajca ter mešamo, dokler se krema ne zgosti. Kremo vlijemo na pečeno testo in pito pečemo še približno 20 minut. Ohlajeno pito postrežemo s stepeno smetano.',
'Osvežilna pita z izrazitim okusom limone.',
17,
2,
8
),

(
'Domač vanilijev sladoled',
240,
'Mleko segrejemo skupaj z vanilijo. Rumenjake stepemo s sladkorjem in jim počasi prilijemo toplo mleko. Zmes kuhamo na nizkem ognju, dokler se ne zgosti. Dodamo sladko smetano in maso popolnoma ohladimo. Sladoled zamrznemo ter ga med zamrzovanjem večkrat premešamo za kremasto teksturo.',
'Kremast domač sladoled z bogatim okusom vanilije.',
13,
2,
5
),

(
'Jabolčni zavitek',
90,
'Testo tanko razvaljamo na kuhinjski krpi. Jabolka olupimo in naribamo ter jim dodamo cimet, sladkor in rozine. Nadev razporedimo po testu in ga previdno zvijemo. Zavitek premažemo z maslom in pečemo približno 40 minut. Pred serviranjem ga posujemo s sladkorjem v prahu.',
'Tradicionalni domači zavitek z jabolki in cimetom.',
19,
3,
9
),

(
'Medenjaki',
60,
'Med segrejemo skupaj z maslom. Dodamo moko, sladkor, jajce in začimbe ter zgnetemo testo. Testo pustimo počivati, nato ga razvaljamo in izrežemo različne oblike. Medenjake pečemo približno 10 minut. Ko se ohladijo, jih lahko okrasimo z belo glazuro.',
'Dišeči praznični piškoti z medom in toplimi začimbami.',
18,
1,
2
),

(
'Palačinke z marmelado',
30,
'Iz moke, mleka in jajc pripravimo gladko maso brez grudic. Na segreti ponvi spečemo tanke palačinke z obeh strani. Še tople namažemo z marmelado in jih zvijemo ali prepognemo. Po želji jih posujemo s sladkorjem v prahu.',
'Klasična domača sladica za hitro pripravo.',
10,
1,
10
),

(
'Bananin kruh',
75,
'Banane pretlačimo z vilico in jih zmešamo z jajci, sladkorjem in stopljenim maslom. Dodamo moko in pecilni prašek. Maso vlijemo v podolgovat model in pečemo približno 50 minut. Ohlajen kruh narežemo na rezine in postrežemo.',
'Sočen kolač z okusom zrelih banan.',
11,
2,
10
),

(
'Makroni',
150,
'Beljake stepemo v trd sneg in postopoma dodajamo sladkor. Primešamo mandljevo moko in maso nežno mešamo do gladke teksture. Z dresirno vrečko oblikujemo kroge na pekaču in jih pustimo počivati 30 minut. Pečemo jih pri nizki temperaturi. Ohlajene makrone napolnimo s čokoladno ali sadno kremo.',
'Elegantni francoski piškoti s hrustljavo skorjico in mehko sredico.',
3,
3,
2
),

(
'Čokoladni sufle',
45,
'Čokolado in maslo stopimo nad paro. Ločeno stepemo jajca in sladkor, nato dodamo stopljeno čokolado in moko. Modelčke namažemo z maslom in jih napolnimo z maso. Sufleje pečemo kratek čas, da sredica ostane tekoča. Postrežemo jih takoj po peki.',
'Topla čokoladna sladica s tekočo sredico.',
7,
3,
4
),

(
'Sadni smoothie',
15,
'Sadje narežemo na manjše koščke in ga damo v blender. Dodamo mleko, led in po želji med. Vse skupaj miksamo, dokler ne dobimo gladke teksture. Smoothie postrežemo dobro ohlajen.',
'Osvežilen sadni napitek za vroče dni.',
9,
1,
7
),

(
'Krofi z marmelado',
120,
'Iz moke, mleka, kvasa in jajc pripravimo kvašeno testo. Testo pustimo vzhajati približno eno uro. Nato oblikujemo krofe in jih ponovno pustimo vzhajati. Krofe ocvremo v vročem olju do zlato rjave barve in jih napolnimo z marmelado.',
'Mehki domači krofi s sladkim marmeladnim nadevom.',
5,
2,
4
),

(
'Čokoladni piškoti',
45,
'Maslo in sladkor penasto stepemo. Dodamo jajce in moko ter primešamo koščke čokolade. Iz mase oblikujemo majhne kupčke in jih pečemo približno 15 minut. Piškoti se med peko rahlo razlezejo in postanejo hrustljavi na robovih.',
'Hrustljavi piškoti s koščki temne čokolade.',
8,
1,
2
)
ON CONFLICT (id) DO UPDATE SET
    ime = EXCLUDED.ime,
    cas_priprave = EXCLUDED.cas_priprave,
    postopek = EXCLUDED.postopek,
    kratek_opis = EXCLUDED.kratek_opis,
    avtor = EXCLUDED.avtor,
    tezavnost = EXCLUDED.tezavnost,
    kategorija = EXCLUDED.kategorija;


-- select * from sladica;




INSERT INTO sestavina (ime, enota)
VALUES
    ('moka', 'g'), ('sladkor', 'g'), ('jajca', ''),
    ('maslo', 'g'), ('temna čokolada', 'g'),
    ('sladka smetana', 'ml'), ('pecilni prašek', 'g'),
    ('mleko', 'ml'), ('vanilijev ekstrakt', 'ml'),
    ('piškoti', 'g'), ('kremni sir', 'g'),
    ('jagode', 'g'), ('kakav', 'g'), ('sadje', 'g'),
    ('kokosova moka', 'g'), ('kondenzirano mleko', 'ml'),
    ('limone', ''), ('kava', 'ml'), ('mascarpone', 'g'),
    ('baby piškoti', 'g'), ('jabolka', 'g'),
    ('cimet', 'g'), ('rozine', 'g'), ('med', 'g'),
    ('marmelada', 'g'), ('banane', ''),
    ('mandljeva moka', 'g'), ('kvas', 'g'),
    ('olje', 'ml'), ('sol', 'g'), ('led', 'kos')
ON CONFLICT (id) DO UPDATE SET
    ime = EXCLUDED.ime,
    enota = EXCLUDED.enota;

-- drop table if exists sestavina cascade;

-- select * from sestavina;

INSERT INTO pripomocek (ime)
VALUES
    ('pečica'), ('mešalnik'), ('tortni model'),
    ('pekač'), ('ponev'), ('kozica'),
    ('blender'), ('dresirna vrečka'),
    ('model za pito'), ('zamrzovalnik')
ON CONFLICT (id) DO UPDATE SET ime = EXCLUDED.ime;

-- select * from pripomocek;

INSERT INTO vsebuje (sladica, sestavina, kolicina_sestavine)
VALUES
    (1,1,200), (1,2,180), (1,3,4), (1,4,150), (1,5,200), (1,6,250),
    (2,1,250), (2,2,120), (2,3,2), (2,7,12), (2,8,200), (2,9,5),
    (3,10,200), (3,4,80), (3,11,500), (3,2,150), (3,12,250),
    (4,1,300), (4,4,200), (4,2,100), (4,3,1),
    (5,5,200), (5,6,250), (5,3,3), (5,2,50),
    (6,1,250), (6,4,150), (6,2,100), (6,14,400),
    (7,18,250), (7,19,500), (7,20,300), (7,3,4), (7,13,15),
    (8,10,300), (8,13,15), (8,15,150), (8,16,200),
    (9,5,200), (9,4,150), (9,2,180), (9,3,3), (9,1,100),
    (10,1,250), (10,4,150), (10,17,3), (10,2,180), (10,3,3),
    (11,8,500), (11,6,250), (11,3,4), (11,2,120), (11,9,5),
    (12,1,300), (12,21,1000), (12,22,5), (12,2,100), (12,23,80),
    (13,1,300), (13,24,150), (13,4,80), (13,2,100), (13,3,1),
    (14,1,250), (14,8,500), (14,3,3), (14,25,200),
    (15,26,3), (15,1,250), (15,2,120), (15,3,2), (15,4,100),
    (16,3,3), (16,2,200), (16,27,120), (16,5,150),
    (17,5,200), (17,4,100), (17,3,3), (17,2,80), (17,1,40),
    (18,14,300), (18,8,200), (18,31,6), (18,24,20),
    (19,1,500), (19,8,250), (19,28,20), (19,3,2), (19,29,1000), (19,25,200),
    (20,4,150), (20,2,120), (20,3,1), (20,1,250), (20,5,150)
ON CONFLICT (sladica, sestavina) DO UPDATE SET
    kolicina_sestavine = EXCLUDED.kolicina_sestavine;

-- select * from vsebuje;

INSERT INTO potrebujes (sladica, pripomocek)
VALUES
    (1,1),(1,2),(1,3), (2,1),(2,2),(2,4), (3,1),(3,2),(3,3),
    (4,1),(4,4), (5,2),(5,6), (6,1),(6,9), (7,2),(7,4),
    (8,2), (9,1),(9,4), (10,1),(10,6),(10,9),
    (11,2),(11,6),(11,10), (12,1),(12,4), (13,1),(13,4),
    (14,2),(14,5), (15,1),(15,4), (16,1),(16,8),
    (17,1),(17,6), (18,7), (19,5),(19,6), (20,1),(20,4)
ON CONFLICT (sladica, pripomocek) DO NOTHING;

-- SELECT * from potrebujes;

-- drop table if exists priljubljeno cascade;


INSERT INTO priljubljeno (sladica, oseba)
VALUES
    (1,7), (1,20), (3,12), (5,13), (7,5),
    (9,8), (12,6), (14,9), (18,19), (20,3), (15,7)
ON CONFLICT (sladica, oseba) DO NOTHING;


INSERT INTO priljubljeno (sladica, oseba)
VALUES
    (1,22), (14,22)
ON CONFLICT (sladica, oseba) DO NOTHING;

-- SELECT * from priljubljeno;

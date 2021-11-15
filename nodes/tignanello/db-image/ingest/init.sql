CREATE DATABASE IF NOT EXISTS tignanello;
USE tignanello;

DROP TABLE IF EXISTS states;

DROP TABLE IF EXISTS transitions;

DROP TABLE IF EXISTS species;

CREATE TABLE states (
	id INTEGER PRIMARY KEY,
        species INTEGER NOT NULL,
	element CHAR(2) NOT NULL,
	nuclearcharge INTEGER NOT NULL,
	ioncharge INTEGER NOT NULL,
        configuration VARCHAR(32),
	s INTEGER,
	l INTEGER,
	j INTEGER,
	energy FLOAT
);

CREATE TABLE species (
	id INTEGER PRIMARY KEY,
	element CHAR(2) NOT NULL,
        nuclearcharge INTEGER NOT NULL,
        ioncharge INTEGER NOT NULL
);

CREATE TABLE transitions (
	initialstate INTEGER NOT NULL,
	finalstate INTEGER NOT NULL,
	wavelength FLOAT,
	log10wosc FLOAT,
	a FLOAT
);


LOAD DATA INFILE '/var/lib/mysql-files/states.out' INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

LOAD DATA INFILE '/var/lib/mysql-files/lines.out' INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

INSERT INTO species (id, element, nuclearcharge, ioncharge)  SELECT DISTINCT species,element,nuclearcharge,ioncharge FROM states;

CREATE USER vamdc;
GRANT select ON *.* to 'vamdc'@'%';

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

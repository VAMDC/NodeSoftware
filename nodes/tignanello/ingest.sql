LOAD DATA LOCAL INFILE 'states.out' INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

LOAD DATA LOCAL INFILE 'lines.out' INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

INSERT INTO species (id, element, nuclearcharge, ioncharge)  SELECT DISTINCT species,element,nuclearcharge,ioncharge FROM states;

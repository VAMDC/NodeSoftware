#replace with correct paths

# load 
LOAD DATA local INFILE '<abspath>/species.out' IGNORE INTO TABLE species COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '<abspath>/references.out' IGNORE INTO TABLE refs COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '<abspath>/states.out' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '<abspath>/transitions.out' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

# single state mapping
#LOAD DATA local INFILE '<abspath>/singlestates.out' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

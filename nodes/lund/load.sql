#replace with correct paths

# load 
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/db_indata/species.in' IGNORE INTO TABLE species COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/db_indata/references.in' IGNORE INTO TABLE refs COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/db_indata/states.in' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/db_indata/transitions.in' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

# single state mapping - uncomment when single-state file is available.
#LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/db_indata/singlestates.in' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

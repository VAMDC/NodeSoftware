#replace with correct paths

# load 
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/species.dat' IGNORE INTO TABLE species COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/references.dat' IGNORE INTO TABLE refs COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/states.dat' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/transitions.dat' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

# single state mapping - uncomment when single state file is available
#LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lund/singlestates.dat' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';

#
# replace with correct paths, then feed to e.g. mysql with 
#
# $ mysql -u <databaseuser> -p < load.sql 
#

LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/ExampleNode/species.in' IGNORE INTO TABLE species COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/ExampleNode/references.in' IGNORE INTO TABLE refs COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/ExampleNode/states.in' IGNORE INTO TABLE states COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
LOAD DATA local INFILE '/home/vamdc/NodeSoftware/nodes/lExampleNode/transitions.in' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"';
-- Make sure to run this file from a mysql started with --verbose option to see what's happening.

alter table transitions disable keys;

load data infile '/vald/vamdc/db_input_files/species.dat' into table species columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/species_components.dat' into table species_components columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/references.dat' ignore into table refs columns terminated by ';' enclosed by '"' ;
load data infile '/vald/vamdc/db_input_files/linelists.dat' ignore into table linelists columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/linelists_references.dat' ignore into table linelists_references columns terminated by ';' optionally enclosed by '"';

alter table states ROW_FORMAT = FIXED;
--alter table states modify id varchar(64) NOT NULL;

load data infile '/vald/vamdc/db_input_files/upstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/lowstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';

--create temporary table `sids` (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, charid VARCHAR(64) NOT NULL UNIQUE);
--insert into sids (charid) select id from states;
--update states,sids set states.id=sids.id where states.id=sids.charid;
--alter table states modify id INT NOT NULL;
alter table transitions ROW_FORMAT = FIXED;

--alter table transitions modify upstate varchar(64);
--alter table transitions modify lostate varchar(64);

load data infile '/vald/vamdc/db_input_files/transitions.dat' ignore into table transitions columns terminated by ';' optionally enclosed by '"';

--update transitions,sids set transitions.upstate=sids.id where transitions.upstate=sids.charid;
update transitions t, states s set t.einsteina=(0.667025*POWER(10,16) * POWER(10,t.loggf)) / ((2.0 * s.j + 1.0) * POWER(t.wavevac,2)) where t.upstate=s.id;

create index speciesid_wave on transitions (species_id, wavevac);
alter table transitions enable keys;
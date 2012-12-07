-- Make sure to run this file from a mysql started with --verbose option to see what's happening.

alter table states ROW_FORMAT = FIXED;
alter table transitions ROW_FORMAT = FIXED;

-- while bibtex file contains mix of cases, we have to recreate refs-table as case-sensitive here
drop table refs;
CREATE TABLE `refs` (`id` varchar(7) NOT NULL,`bibtex` longtext,PRIMARY KEY (`id`)) ENGINE=MyISAM COLLATE utf8_bin;
load data infile '/vald/vamdc/db_input_files/references.dat' ignore into table refs columns terminated by ';' enclosed by '"' ;

load data infile '/vald/vamdc/db_input_files/species.dat' into table species columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/species_components.dat' into table species_components columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/linelists.dat' ignore into table linelists columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/linelists_references.dat' ignore into table linelists_references columns terminated by ';' optionally enclosed by '"';

load data infile '/vald/vamdc/db_input_files/upstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/lowstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';

load data infile '/vald/vamdc/db_input_files/transitions.dat' ignore into table transitions columns terminated by ';' optionally enclosed by '"';

update transitions t, states s set t.einsteina=(0.667025*POWER(10,16) * POWER(10,t.loggf)) / ((2.0 * s.j + 1.0) * POWER(t.wave,2)) where t.upstate=s.id;

-- an index over these two tables speeds up usual queries
create index speciesid_wave on transitions (species_id, wavevac);


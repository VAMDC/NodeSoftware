set foreign_key_checks=0;
load data infile '/vald/species.dat' into table species columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/references.dat' ignore into table refs columns terminated by ';' enclosed by '"' ;
load data infile '/vald/linelists.dat' ignore into table linelists columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/linelists2references_manytomany.dat' ignore into table linelists_references columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/states.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/transitions.dat' ignore into table transitions columns terminated by ';' optionally enclosed by '"';


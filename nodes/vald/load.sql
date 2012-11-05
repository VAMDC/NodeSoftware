-- Make sure to run this file from a mysql started with --verbose option to see what's happening.

alter table states ROW_FORMAT = FIXED;
alter table transitions ROW_FORMAT = FIXED;

load data infile '/vald/vamdc/db_input_files/species.dat' into table species columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/species_components.dat' into table species_components columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/references.dat' ignore into table refs columns terminated by ';' enclosed by '"' ;
load data infile '/vald/vamdc/db_input_files/linelists.dat' ignore into table linelists columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/linelists_references.dat' ignore into table linelists_references columns terminated by ';' optionally enclosed by '"';

load data infile '/vald/vamdc/db_input_files/upstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/lowstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';

load data infile '/vald/vamdc/db_input_files/transitions.dat' ignore into table transitions columns terminated by ';' optionally enclosed by '"';

update transitions t, states s set t.einsteina=(0.667025*POWER(10,16) * POWER(10,t.loggf)) / ((2.0 * s.j + 1.0) * POWER(t.wave,2)) where t.upstate=s.id;

-- create the mapping transitions <-> references for quick ref
-- retrieval during querying
insert into transitions_references (trans_id, ref_id)(select id, wave_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select id, waveritz_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select id, loggf_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select id, gammarad_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select id, gammastark_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select id, waals_ref_id from transitions);
insert into transitions_references (trans_id, ref_id)(select transitions.id,states.energy_ref_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
insert into transitions_references (trans_id, ref_id)(select transitions.id,states.lande_ref_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
insert into transitions_references (trans_id, ref_id)(select transitions.id,states.level_ref_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
-- creating the index here
create index tidx on transitions_references (trans_id);


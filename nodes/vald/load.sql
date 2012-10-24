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

insert into trans_refs (select id, wavevac_ref_id from transitions);

update transitions t, states s set t.einsteina=(0.667025*POWER(10,16) * POWER(10,t.loggf)) / ((2.0 * s.j + 1.0) * POWER(t.wave,2)) where t.upstate=s.id;

-- create the mapping transitions - references and link all references
-- to the correct transition
create table trans_refs (trans_id bigint, ref_id varchar(7));
insert into trans_refs (select id, wave_ref_id from transitions);
insert into trans_refs (select id, waveritz_ref_id from transitions);
insert into trans_refs (select id, loggf_ref_id from transitions);
insert into trans_refs (select id, gammarad_ref_id from transitions);
insert into trans_refs (select id, gammastark_ref_id from transitions);
insert into trans_refs (select id, waals_ref_id from transitions);
insert into trans_refs (select transitions.id,states.energy_ref_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
insert into trans_refs (select transitions.id,states.lande_ref_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
insert into trans_refs (select transitions.id,states.level_id from transitions,states where transitions.upstate=states.id or transitions.lostate=states.id);
create index tidx on trans_refs (trans_id);


-- fixing a mal-named bibtex reference (kept here for reference, remove
-- if fixed in raw data dump next update)
update transitions t set t.wave_ref_id="K11" where t.wave_ref_id="K11P";
update transitions t set t.waveritz_ref_id="K11" where t.waveritz_ref_id="K11P";
update transitions t set t.loggf_ref_id="K11" where t.loggf_ref_id="K11P";
update transitions t set t.gammarad_ref_id="K11" where t.gammarad_ref_id="K11P";
update transitions t set t.gammastark_ref_id="K11" where t.gammastark_ref_id="K11P";
update transitions t set t.waals_ref_id="K11" where t.waals_ref_id="K11P";
update states s set s.energy_ref_id="K11" where s.energy_ref_id="K11P";
update states s set s.lande_ref_id="K11" where s.lande_ref_id="K11P";
update states s set s.level_ref_id="K11" where s.level_ref_id="K11P";

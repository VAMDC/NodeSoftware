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

create index speciesid_wave on transitions (species_id, wave);

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

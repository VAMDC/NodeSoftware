create temporary table `sids` (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, charid VARCHAR(255) NOT NULL UNIQUE);
insert into sids (charid) select id from states;
update states,sids set states.id=sids.id where states.id=sids.charid;
alter table states modify id INT NOT NULL;
update transitions,sids set transitions.upstate=sids.id where transitions.upstate=sids.charid;
update transitions,sids set transitions.lostate=sids.id where transitions.lostate=sids.charid;
alter table transitions modify upstate INT;
alter table transitions modify lostate INT;


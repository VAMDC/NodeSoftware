from django.db import models
import fake

class DataSource(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField()
	id_biblio = models.IntegerField()
	biblio_index = models.TextField(blank=True)
	owner = models.CharField(max_length=32)
	type = models.IntegerField()
	status = models.CharField(max_length=8)
	pub_time_ds = models.DateTimeField()

	def getMethod(self):
		return fake.methods[self.type].id

	class Meta:
		abstract = True


class EnergyDataSource(DataSource):
	id_energy_ds = models.IntegerField(primary_key=True)

	def __unicode__(self):
		return u'ID:%s %s ' % (self.id_energy_ds, self.name)

	class Meta(DataSource.Meta):
		abstract = True
		db_table = 'energy_ds'


class TransitionDataSource(DataSource):
	id_transition_ds = models.IntegerField(primary_key=True)
	composition = models.CharField(max_length=7)

	def __unicode__(self):
		return u'ID:%s %s ' % (self.id_transition_ds, self.name)

	class Meta(DataSource.Meta):
		abstract = True
		db_table = 'transition_ds'


class LineprofDataSource(DataSource):
	id_transition_ds = models.IntegerField(primary_key=True, db_column='id_lineprof_ds')
	composition = models.CharField(max_length=7)
	temperature = models.FloatField()
	pressure = models.FloatField()

	def __unicode__(self):
		return u'ID:%s %s ' % (self.id_transition_ds, self.name)

	class Meta(DataSource.Meta):
		abstract = True
		db_table = 'lineprof_ds'


PREFIX = None
def getPrefix():
	return PREFIX

class Data(models.Model):
	id_substance = models.IntegerField()

	def getCase(self):
		return getPrefix()

	class Meta:
		abstract = True


class EnergyData(Data):
	id_energy = models.BigIntegerField(primary_key=True)
	id_energy_ds = None
	energy = models.FloatField()
	energy_delta = models.FloatField(null=True, blank=True)
	defining_tr_n = models.IntegerField(null=True, blank=True)

	def qns(self):
		return []

	def __unicode__(self):
		return u'ID:%s %s %s =%s=%s=' % (self.id_energy, self.id_energy_ds, self.id_substance, self.energy, self.energy_delta)

	class Meta(Data.Meta):
		abstract = True
		db_table = 'energy'

class Data2(Data):
	id_transition = None
	id_transition_ds = None
	wavenumber = None
	wavenumber_err = None
	einstein_coefficient = None
	einstein_coefficient_err = None
	intensity = None
	intensity_err = None
	
	up = 0
	low = 0

	def up(self):
		return []

	def low(self):
		return []

	class Meta(Data.Meta):
		abstract = True


class TransitionData(Data2):
	id_transition = models.BigIntegerField(primary_key=True, db_column='id_transition')
	wavenumber = models.FloatField(db_column='wave_number')
	wavenumber_err = models.FloatField(db_column='wave_number_uc', null=True, blank=True)
	einstein_coefficient = models.FloatField(db_column='einstein_coefficient', null=True, blank=True)
	einstein_coefficient_err = models.FloatField(db_column='einstein_coefficient_uc', null=True, blank=True)

	def __unicode__(self):
		return u'ID:%s %s %s =%s=%s=%s=%s=' % (self.id_transition, self.id_transition_ds, self.id_substance, self.wavenumber, self.wavenumber_err, self.einstein_coefficient, self.einstein_coefficient_err)

	class Meta(Data2.Meta):
		abstract = True
		db_table = 'transition'


class LineprofData(Data2):
	id_transition = models.BigIntegerField(primary_key=True, db_column='id_lineprof')
	wavenumber = models.FloatField(db_column='wavelength')
	wavenumber_err = models.FloatField(db_column='wavelength_err', null=True, blank=True)
	intensity = models.FloatField(null=True, blank=True)
	intensity_err = models.FloatField(null=True, blank=True)

	def __unicode__(self):
		return u'ID:%s %s %s =%s=%s=%s=%s=' % (self.id_transition, self.id_transition_ds, self.id_substance, self.wavenumber, self.wavenumber_err, self.intensity, self.intensity_err)

	class Meta(Data2.Meta):
		abstract = True
		db_table = 'lineprof'


class LineprofHsA(models.Model):
	id_transition = None
	id_substance_act = models.IntegerField()
	halfwidth = models.FloatField(null=True, blank=True)
	halfwidth_err = models.FloatField(null=True, blank=True)
	halfwidth_td = models.FloatField(null=True, blank=True)
	halfwidth_td_err = models.FloatField(null=True, blank=True)
	shift = models.FloatField(null=True, blank=True)
	shift_err = models.FloatField(null=True, blank=True)
	shift_td = models.FloatField(null=True, blank=True)
	shift_td_err = models.FloatField(null=True, blank=True)

	def __unicode__(self):
		return u'ID:%s %s =%s=%s=%s=%s=' % (self.id_transition, self.id_substance_act, self.halfwidth, self.halfwidth_td, self.shift, self.shift_td)

	class Meta:
		abstract = True
		db_table = 'lineprof_hs'


class LineprofPpA(models.Model):
	id_transition_ds = None
	substance_act = models.IntegerField(unique=True)
	p_pressure = models.FloatField()

	def __unicode__(self):
		return u'ID:%s %s' % (self.id_transition_ds, self.substance_act)

	class Meta:
		abstract = True
		db_table = 'lineprof_pp'





class EnergyDigestA(models.Model):
	id_energy_ds = None
	id_substance = models.IntegerField()
	energy_min = models.FloatField()
	energy_max = models.FloatField()
	line_count = models.BigIntegerField()
	flags = models.CharField(max_length=62)
	pub_time = models.DateTimeField()

	def __unicode__(self):
		return u'ID:%s %s' % (self.id_energy_ds, self.id_substance)

	class Meta:
		abstract = True
		db_table = 'energy_digest'


class TransitionDigestA(models.Model):
	id_transition_ds = None
	id_substance = models.IntegerField()
	wavenumber_min = models.FloatField(db_column='wave_number_min')
	wavenumber_max = models.FloatField(db_column='wave_number_max   ')
	line_count = models.BigIntegerField()
	flags = models.CharField(max_length=78)
	pub_time = models.DateTimeField()

	def __unicode__(self):
		return u'ID:%s %s' % (self.id_transition_ds, self.id_substance)

	class Meta:
		abstract = True
		db_table = 'transition_digest'


class LineprofDigestA(models.Model):
	id_transition_ds = None
	id_substance = models.IntegerField()
	wavenumber_min = models.FloatField(db_column='wavelength_min')
	wavenumber_max = models.FloatField(db_column='wavelength_max')
	intensity_min = models.FloatField(null=True, blank=True)
	intensity_max = models.FloatField(null=True, blank=True)
	intensity_sum = models.FloatField(null=True, blank=True)
	line_count = models.BigIntegerField()
	flags = models.CharField(max_length=57)
	pub_time = models.DateTimeField()

	def __unicode__(self):
		return u'ID:%s %s' % (self.id_transition_ds, self.id_substance)

	class Meta:
		abstract = True
		db_table = 'lineprof_digest'


class LineprofHsDigestA(models.Model):
	id_transition_ds = None
	id_substance = models.IntegerField()
	id_substance_act = models.IntegerField()
	flags = models.CharField(max_length=91)

	def __unicode__(self):
		return u'ID:%s %s %s=%s=' % (self.id_transition_ds, self.id_substance, self.id_substance_act, self.flags)

	class Meta:
		abstract = True
		db_table = 'lineprof_hs_digest'







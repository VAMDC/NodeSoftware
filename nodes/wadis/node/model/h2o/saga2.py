from node.model.data import *

prefix = 'nltcs'


class EnergyDs(EnergyDataSource):
	class Meta(EnergyDataSource.Meta):
		pass



class Energy(EnergyData):
	id_energy_ds = models.ForeignKey(EnergyDs, db_column = 'id_energy_ds')
	ident_nm = models.CharField(max_length = 64, blank = True)
	ident_nm_f = models.IntegerField()


	def qns(self):
		qns = [None] * 6
		if self.ident_nm is not None:
			qns = self.ident_nm.split()
		return [["v1", qns[0]], ["v2", qns[1]], ["v3", qns[2]], ["J", qns[3]], ["Ka", qns[4]], ["Kc", qns[5]]]


	class Meta(EnergyData.Meta):
		pass



class TransitionDs(TransitionDataSource):
	class Meta(TransitionDataSource.Meta):
		pass



class Transition(TransitionData):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')
	wavenumber = models.FloatField(db_column = 'wave_number')
	wavenumber_err = models.FloatField(db_column = 'wave_number_uc', null = True, blank = True)
	einstein_coefficient = models.FloatField(db_column = 'einstein_coefficient', null = True, blank = True)
	einstein_coefficient_err = models.FloatField(db_column = 'einstein_coefficient_uc', null = True, blank = True)
	ident_nm_upr_j = models.IntegerField(null = True, blank = True)
	ident_nm_upr_ka = models.IntegerField(null = True, blank = True)
	ident_nm_upr_kc = models.IntegerField(null = True, blank = True)
	ident_nm_upr_v1 = models.IntegerField(null = True, blank = True)
	ident_nm_upr_v2 = models.IntegerField(null = True, blank = True)
	ident_nm_upr_v3 = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_j = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_ka = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_kc = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_v1 = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_v2 = models.IntegerField(null = True, blank = True)
	ident_nm_lwr_v3 = models.IntegerField(null = True, blank = True)
	ident_nm_f = models.IntegerField()


	def up(self):
		return [["v1", self.ident_nm_upr_v1], ["v2", self.ident_nm_upr_v2], ["v3", self.ident_nm_upr_v3], ["J", self.ident_nm_upr_j], ["Ka", self.ident_nm_upr_ka], ["Kc", self.ident_nm_upr_kc]]


	def low(self):
		return [["v1", self.ident_nm_lwr_v1], ["v2", self.ident_nm_lwr_v2], ["v3", self.ident_nm_lwr_v3], ["J", self.ident_nm_lwr_j], ["Ka", self.ident_nm_lwr_ka], ["Kc", self.ident_nm_lwr_kc]]


	class Meta(TransitionData.Meta):
		pass



class LineprofDs(LineprofDataSource):
	class Meta(LineprofDataSource.Meta):
		pass



class Lineprof(LineprofData):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')
	ident_nm_lo_v1 = models.IntegerField(null = True, blank = True)
	ident_nm_lo_v2 = models.IntegerField(null = True, blank = True)
	ident_nm_lo_v3 = models.IntegerField(null = True, blank = True)
	ident_nm_lo_j = models.IntegerField(null = True, blank = True)
	ident_nm_lo_ka = models.IntegerField(null = True, blank = True)
	ident_nm_lo_kc = models.IntegerField(null = True, blank = True)
	ident_nm_up_v1 = models.IntegerField(null = True, blank = True)
	ident_nm_up_v2 = models.IntegerField(null = True, blank = True)
	ident_nm_up_v3 = models.IntegerField(null = True, blank = True)
	ident_nm_up_j = models.IntegerField(null = True, blank = True)
	ident_nm_up_ka = models.IntegerField(null = True, blank = True)
	ident_nm_up_kc = models.IntegerField(null = True, blank = True)
	ident_nm_f = models.IntegerField()


	def up(self):
		return [["v1", self.ident_nm_up_v1], ["v2", self.ident_nm_up_v2], ["v3", self.ident_nm_up_v3], ["J", self.ident_nm_up_j], ["Ka", self.ident_nm_up_ka], ["Kc", self.ident_nm_up_kc]]


	def low(self):
		return [["v1", self.ident_nm_lo_v1], ["v2", self.ident_nm_lo_v2], ["v3", self.ident_nm_lo_v3], ["J", self.ident_nm_lo_j], ["Ka", self.ident_nm_lo_ka], ["Kc", self.ident_nm_lo_kc]]


	class Meta(LineprofData.Meta):
		pass



class LineprofHs(LineprofHsA):
	id_transition = models.ForeignKey(Lineprof, db_column = 'id_lineprof')


	class Meta(LineprofHsA.Meta):
		pass



class LineprofPp(LineprofPpA):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')


	class Meta(LineprofPpA.Meta):
		pass



class EnergyDigest(EnergyDigestA):
	id_energy_ds = models.ForeignKey(EnergyDs, db_column = 'id_energy_ds')


	class Meta(EnergyDigestA.Meta):
		pass



class TransitionDigest(TransitionDigestA):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')
	wavenumber_min = models.FloatField(db_column = 'wave_number_min')
	wavenumber_max = models.FloatField(db_column = 'wave_number_max   ')


	class Meta(TransitionDigestA.Meta):
		pass



class LineprofDigest(LineprofDigestA):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')


	class Meta(LineprofDigestA.Meta):
		pass



class LineprofHsDigestA(LineprofHsDigestA):
	id_transition_ds = models.ForeignKey(LineprofDigest, db_column = 'id_transition_ds')


	class Meta(LineprofHsDigestA.Meta):
		pass

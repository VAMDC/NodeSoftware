from node.model.data import *


prefix = 'dcs'


class EnergyDs(EnergyDataSource):
	class Meta(EnergyDataSource.Meta):
		pass



class Energy(EnergyData):
	id_energy_ds = models.ForeignKey(EnergyDs, db_column = 'id_energy_ds')
	ident = models.CharField(max_length = 20, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def qns(self):
		qns = [None] * 2
		if self.ident_nm is not None:
			qns = self.ident_nm.split()
		return [["v", qns[0]], ["J", qns[2]]]


	class Meta(EnergyData.Meta):
		pass



class TransitionDs(TransitionDataSource):
	class Meta(TransitionDataSource.Meta):
		pass



class Transition(TransitionDataW):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')
	ident_lo_nu = models.IntegerField(null = True, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_up_nu = models.IntegerField(null = True, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["v", self.ident_up_nu], ["J", self.ident_up_j]]


	def low(self):
		return [["v", self.ident_lo_nu], ["J", self.ident_lo_j]]


	class Meta(TransitionData.Meta):
		pass



class LineprofDs(LineprofDataSource):
	class Meta(LineprofDataSource.Meta):
		pass



class Lineprof(LineprofData):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')
	ident_lo_nu = models.IntegerField(null = True, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_up_nu = models.IntegerField(null = True, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["v", self.ident_up_nu], ["J", self.ident_up_j]]


	def low(self):
		return [["v", self.ident_lo_nu], ["J", self.ident_lo_j]]


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



class TransitionDigest(TransitionDigestAW):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')


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


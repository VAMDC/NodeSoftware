from wadis.node.model.data import *

prefix = 'ltcs'


class EnergyDs(EnergyDataSource):
	class Meta(EnergyDataSource.Meta):
		pass



class Energy(EnergyData):
	id_energy_ds = models.ForeignKey(EnergyDs, db_column = 'id_energy_ds')
	ident = models.CharField(max_length = 20, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def qns(self):
		qns = [None] * 6
		if self.ident_nm is not None:
			qns = self.ident_nm.split()
		return [["v1", qns[0]], ["v2", qns[1]], ["l2", qns[2]], ["v3", qns[3]], ["J", qns[4]], ["kronigParity", qns[5]]]


	class Meta(EnergyData.Meta):
		pass



class TransitionDs(TransitionDataSource):
	class Meta(TransitionDataSource.Meta):
		pass



class Transition(TransitionDataW):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')
	ident_lo_n1 = models.IntegerField(null = True, blank = True)
	ident_lo_n2 = models.IntegerField(null = True, blank = True)
	ident_lo_l2 = models.IntegerField(null = True, blank = True)
	ident_lo_n3 = models.IntegerField(null = True, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_lo_sym = models.CharField(max_length = 1, blank = True)
	ident_up_n1 = models.IntegerField(null = True, blank = True)
	ident_up_n2 = models.IntegerField(null = True, blank = True)
	ident_up_l2 = models.IntegerField(null = True, blank = True)
	ident_up_n3 = models.IntegerField(null = True, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_up_sym = models.CharField(max_length = 1, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["v1", self.ident_up_n1], ["v2", self.ident_up_n2], ["l2", self.ident_up_l2], ["v3", self.ident_up_n3], ["J", self.ident_up_j], ["kronigParity", self.ident_up_sym]]


	def low(self):
		return [["v1", self.ident_lo_n1], ["v2", self.ident_lo_n2], ["l2", self.ident_lo_l2], ["v3", self.ident_lo_n3], ["J", self.ident_lo_j], ["kronigParity", self.ident_lo_sym]]


	class Meta(TransitionData.Meta):
		pass



class LineprofDs(LineprofDataSource):
	class Meta(LineprofDataSource.Meta):
		pass



class Lineprof(LineprofData):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')
	ident_lo_n1 = models.IntegerField(null = True, blank = True)
	ident_lo_n2 = models.IntegerField(null = True, blank = True)
	ident_lo_l2 = models.IntegerField(null = True, blank = True)
	ident_lo_n3 = models.IntegerField(null = True, blank = True)
	ident_lo_sym = models.CharField(max_length = 1, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_up_n1 = models.IntegerField(null = True, blank = True)
	ident_up_n2 = models.IntegerField(null = True, blank = True)
	ident_up_l2 = models.IntegerField(null = True, blank = True)
	ident_up_n3 = models.IntegerField(null = True, blank = True)
	ident_up_sym = models.CharField(max_length = 1, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["v1", self.ident_up_n1], ["v2", self.ident_up_n2], ["l2", self.ident_up_l2], ["v3", self.ident_up_n3], ["J", self.ident_up_j], ["kronigParity", self.ident_up_sym]]


	def low(self):
		return [["v1", self.ident_lo_n1], ["v2", self.ident_lo_n2], ["l2", self.ident_lo_l2], ["v3", self.ident_lo_n3], ["J", self.ident_lo_j], ["kronigParity", self.ident_lo_sym]]


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



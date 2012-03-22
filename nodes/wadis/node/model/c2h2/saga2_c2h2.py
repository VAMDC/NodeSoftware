from wadis.node.model.data import *

prefix = 'lpcs'


class EnergyDs(EnergyDataSource):
	class Meta(EnergyDataSource.Meta):
		pass



class Energy(EnergyData):
	id_energy_ds = models.ForeignKey(EnergyDs, db_column = 'id_energy_ds')
	ident = models.CharField(max_length = 20, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def qns(self):
		qns = [None] * 11
		if self.ident_nm is not None:
			qns = self.ident_nm.split()
		return [["viMode", [1, 2, 3, 4, 5]], ["vi", [qns[0], qns[1], qns[2], qns[3], qns[4]]], ["l", qns[5]], ["r", None if qns[6] == '_' else qns[6]], ["J", qns[7]], ["vibInv", qns[8]], ["parity", None if qns[9] == '_' else qns[9]], ["kronigParity", qns[10]]]


	class Meta(EnergyData.Meta):
		pass



class TransitionDs(TransitionDataSource):
	class Meta(TransitionDataSource.Meta):
		pass



class Transition(TransitionDataW):
	id_transition_ds = models.ForeignKey(TransitionDs, db_column = 'id_transition_ds')
	ident_lo_nu1 = models.IntegerField(null = True, blank = True)
	ident_lo_nu2 = models.IntegerField(null = True, blank = True)
	ident_lo_nu3 = models.IntegerField(null = True, blank = True)
	ident_lo_nu4 = models.IntegerField(null = True, blank = True)
	ident_lo_nu5 = models.IntegerField(null = True, blank = True)
	ident_lo_l = models.IntegerField(null = True, blank = True)
	ident_lo_r = models.CharField(max_length = 1, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_lo_sym = models.CharField(max_length = 1, blank = True)
	ident_lo_sym2 = models.CharField(max_length = 1, blank = True)
	ident_lo_epsilon = models.CharField(max_length = 1, blank = True)
	ident_up_nu1 = models.IntegerField(null = True, blank = True)
	ident_up_nu2 = models.IntegerField(null = True, blank = True)
	ident_up_nu3 = models.IntegerField(null = True, blank = True)
	ident_up_nu4 = models.IntegerField(null = True, blank = True)
	ident_up_nu5 = models.IntegerField(null = True, blank = True)
	ident_up_l = models.IntegerField(null = True, blank = True)
	ident_up_r = models.CharField(max_length = 1, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_up_sym = models.CharField(max_length = 1, blank = True)
	ident_up_sym2 = models.CharField(max_length = 1, blank = True)
	ident_up_epsilon = models.CharField(max_length = 1, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["viMode", [1, 2, 3, 4, 5]], ["vi", [self.ident_up_nu1, self.ident_up_nu2, self.ident_up_nu3, self.ident_up_nu4, self.ident_up_nu5]], ["l", self.ident_up_l], ["r", None if self.ident_up_r == '_' else self.ident_up_r], ["J", self.ident_up_j], ["vibInv", self.ident_up_sym], ["parity", None if self.ident_up_sym2 == '_' else self.ident_up_sym2], ["kronigParity", self.ident_up_epsilon]]


	def low(self):
		return [["viMode", [1, 2, 3, 4, 5]], ["vi", [self.ident_lo_nu1, self.ident_lo_nu2, self.ident_lo_nu3, self.ident_lo_nu4, self.ident_lo_nu5]], ["l", self.ident_lo_l], ["r", None if self.ident_lo_r == '_' else self.ident_lo_r], ["J", self.ident_lo_j], ["vibInv", self.ident_lo_sym], ["parity", None if self.ident_lo_sym2 == '_' else self.ident_lo_sym2], ["kronigParity", self.ident_lo_epsilon]]


	class Meta(TransitionData.Meta):
		pass



class LineprofDs(LineprofDataSource):
	class Meta(LineprofDataSource.Meta):
		pass



class Lineprof(LineprofData):
	id_transition_ds = models.ForeignKey(LineprofDs, db_column = 'id_lineprof_ds')
	ident_lo_nu1 = models.IntegerField(null = True, blank = True)
	ident_lo_nu2 = models.IntegerField(null = True, blank = True)
	ident_lo_nu3 = models.IntegerField(null = True, blank = True)
	ident_lo_nu4 = models.IntegerField(null = True, blank = True)
	ident_lo_nu5 = models.IntegerField(null = True, blank = True)
	ident_lo_l = models.IntegerField(null = True, blank = True)
	ident_lo_r = models.CharField(max_length = 1, blank = True)
	ident_lo_j = models.IntegerField(null = True, blank = True)
	ident_lo_sym = models.CharField(max_length = 1, blank = True)
	ident_lo_sym2 = models.CharField(max_length = 1, blank = True)
	ident_lo_epsilon = models.CharField(max_length = 1, blank = True)
	ident_up_nu1 = models.IntegerField(null = True, blank = True)
	ident_up_nu2 = models.IntegerField(null = True, blank = True)
	ident_up_nu3 = models.IntegerField(null = True, blank = True)
	ident_up_nu4 = models.IntegerField(null = True, blank = True)
	ident_up_nu5 = models.IntegerField(null = True, blank = True)
	ident_up_l = models.IntegerField(null = True, blank = True)
	ident_up_r = models.CharField(max_length = 1, blank = True)
	ident_up_j = models.IntegerField(null = True, blank = True)
	ident_up_sym = models.CharField(max_length = 1, blank = True)
	ident_up_sym2 = models.CharField(max_length = 1, blank = True)
	ident_up_epsilon = models.CharField(max_length = 1, blank = True)
	ident_br = models.CharField(max_length = 1, blank = True)
	ident_f = models.IntegerField()
	calc_f = models.IntegerField()


	def up(self):
		return [["viMode", [1, 2, 3, 4, 5]], ["vi", [self.ident_up_nu1, self.ident_up_nu2, self.ident_up_nu3, self.ident_up_nu4, self.ident_up_nu5]], ["l", self.ident_up_l], ["r", None if self.ident_up_r == '_' else self.ident_up_r], ["J", self.ident_up_j], ["vibInv", self.ident_up_sym], ["parity", None if self.ident_up_sym2 == '_' else self.ident_up_sym2], ["kronigParity", self.ident_up_epsilon]]


	def low(self):
		return [["viMode", [1, 2, 3, 4, 5]], ["vi", [self.ident_lo_nu1, self.ident_lo_nu2, self.ident_lo_nu3, self.ident_lo_nu4, self.ident_lo_nu5]], ["l", self.ident_lo_l], ["r", None if self.ident_lo_r == '_' else self.ident_lo_r], ["J", self.ident_lo_j], ["vibInv", self.ident_lo_sym], ["parity", None if self.ident_lo_sym2 == '_' else self.ident_lo_sym2], ["kronigParity", self.ident_lo_epsilon]]


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



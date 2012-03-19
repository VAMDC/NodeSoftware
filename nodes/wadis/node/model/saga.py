import re
from django.db import models
from nodes.wadis.util import inchi


class Substance(models.Model):
	id_substance = models.IntegerField(db_column = 'ID_substance', primary_key = True) # Field name made lowercase.
	type = models.CharField(max_length = 8)
	russian = models.CharField(max_length = 64)
	english = models.CharField(max_length = 64)
	weight = models.FloatField()


	def __unicode__(self):
		return u'ID:%d %s' % (self.id_substance, self.english)


	class Meta:
		db_table = u'Substance'



class Substancecorr(models.Model):
	id_substance = models.IntegerField(db_column = 'ID_substance', primary_key = True) # Field name made lowercase.
	plain_name = models.TextField(blank = True)
	html_name = models.TextField(blank = True)
	id_inchi = models.TextField(blank = True)
	id_inchi_key = models.TextField(blank = True)
	id_subst_main = models.IntegerField(db_column = 'ID_subst_main') # Field name made lowercase.
	id_class_sp = models.IntegerField()
	id_class_gs = models.IntegerField()
	id_class_mt = models.IntegerField()
	meta_vibr = models.CharField(max_length = 120)
	meta_rotat = models.CharField(max_length = 120)
	database_name = models.CharField(max_length = 16, blank = True)
	group_access = models.TextField(blank = True)
	substance_act = models.CharField(max_length = 1)


	def getCharge(self):
		patternObj = re.compile(r"/q([+-]\d+)")
		m = patternObj.search(self.id_inchi) if self.id_inchi is not None else None
		return "0" if m is None else m.group(1)


	def getLatexFormula(self):
		# See http://www.physicsforums.com/misc/howtolatex.pdf
		# See http://vamdc.org/documents/standards/dataModel/vamdcxsams/speciesMolecules.html#molecule

		if self.plain_name is None:
			return None


		def setSubSup(matchObj):
			str = ''
			if matchObj.group(2):
				s = matchObj.group(2)
				if int(s) > 1:
					str += "^" + ("{%s}" % s if len(s) > 1 else s)
			str += matchObj.group(3)
			if matchObj.group(4):
				s = matchObj.group(4)
				if int(s) > 1:
					str += "_" + ("{%s}" % s if len(s) > 1 else s)
			return str


		def setPlusMinus(matchObj):
			str = ''
			if matchObj.group(1):
				s = matchObj.group(1)
				if int(s) > 1:
					str += s
			if matchObj.group(2):
				s = matchObj.group(2)
				if s == 'plus':
					str += '+'
				elif s == 'minus':
					str += '-'
			str = "^" + ("{%s}" % str if len(str) > 1 else str)
			return str


		latexFormula = self.plain_name
		latexFormula = re.sub(r"(_(\d+))?([A-Z][a-z]*)(\d*)", setSubSup, latexFormula)
		latexFormula = re.sub(r"_(\d*)(plus|minus)", setPlusMinus, latexFormula)
		return "$" + latexFormula + "$"


	def getABCFormula(self):
		# See http://vamdc.org/documents/standards/dataModel/vamdcxsams/speciesMolecules.html#molecule
		if self.plain_name is None:
			return None

		abcFormula = self.plain_name
		chargeMatchObj = re.search(r"_(\d*)(plus|minus)", abcFormula)
		charge = (None, None)
		if chargeMatchObj is not None:
			charge = chargeMatchObj.groups()


		def setOnlyMainIsotope(matchObj):
			str = ''
			s = matchObj.group(3)
			if s in ["D", "T"]:
				s = "H"
			str += s
			if matchObj.group(4):
				str += matchObj.group(4)
			else:
				str += "1"
			return str


		abcFormula = re.sub(r"(_(\d+))?([A-Z][a-z]*)(\d*)(_(\d*)(plus|minus))?", setOnlyMainIsotope, abcFormula)
		atomsOfMolecule = re.split(r"([A-Z][a-z]*)", abcFormula)
		atom = None
		atoms = {}
		for atomOfMolecule in atomsOfMolecule:
			if atomOfMolecule:
				if atom:
					if atom in atoms:
						atoms[atom] += int(atomOfMolecule)
					else:
						atoms[atom] = int(atomOfMolecule)
					atom = None
				else:
					atom = atomOfMolecule

		abcFormula = ''
		for atom in sorted(atoms.keys()):
			abcFormula += atom + (str(atoms[atom]) if atoms[atom] > 1 else '')

		abcFormula += (( '-'if charge[1] == 'minus' else '+') if charge[1] else '') + (charge[0] if charge[0] else '')
		return abcFormula


	def __unicode__(self):
		return u'ID:%d %s %s' % (self.id_substance, self.plain_name, self.id_inchi)


	class Meta:
		db_table = u'SubstanceCorr'



class SubstanceDict():
	byId = {}
	byInchi = {}
	byInchiKey = {}

	for substance in Substancecorr.objects.all():
		if substance.id_inchi:
			if not substance.id_inchi_key:
				substance.id_inchi_key = inchi.inchiToInchiKey(str(substance.id_inchi))
				substance.save()
			if not substance.group_access:
				byId[substance.id_substance] = substance
				byInchi[substance.id_inchi] = substance
				byInchiKey[substance.id_inchi_key] = substance



class ClassGs(models.Model):
	id_class_gs = models.IntegerField(primary_key = True)
	name_eng = models.CharField(max_length = 200)
	name_rus = models.CharField(max_length = 200)


	def __unicode__(self):
		return u'ID:%d %s' % (self.id_class_gs, self.name_eng)


	class Meta:
		db_table = u'class_gs'



class ClassMt(models.Model):
	id_class_mt = models.IntegerField(primary_key = True)
	name_eng = models.CharField(max_length = 200)
	name_rus = models.CharField(max_length = 200)


	def __unicode__(self):
		return u'ID:%d %s' % (self.id_class_mt, self.name_eng)


	class Meta:
		db_table = u'class_mt'



class ClassSp(models.Model):
	id_class_sp = models.IntegerField(primary_key = True)
	name_eng = models.CharField(max_length = 200)
	name_rus = models.CharField(max_length = 200)


	def __unicode__(self):
		return u'ID:%d %s' % (self.id_class_sp, self.name_eng)


	class Meta:
		db_table = u'class_sp'

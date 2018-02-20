from openbabel import OBConversion,OBMol


class InchiInfo:

    def __init__(self,inchi):
        self.obconversion = OBConversion()
        self.obconversion.SetInFormat("inchi")
        self.obmol = OBMol()

        self.obconversion.ReadString(self.obmol, inchi)

        self.totalCharge = self.obmol.GetTotalCharge()
        self.formula = self.obmol.GetFormula()
        self.weight = self.obmol.GetMolWt( )

    def getNumAtoms(self):
        return self.obmol.NumAtoms()

    def getAtoms(self,idx):
        return self.GetAtom(idx)

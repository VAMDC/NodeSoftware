# hitran_prm.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk

class HITRANPrm:

    def __init__(self):
        self.name = None
        self.value = None
        self.error = None
        self.ref = None

    @classmethod
    def parse_from_mysql(self, row):
        """
        Parse a MySQL row from the prms table of the HITRAN database
        for information about a HITRAN parameter and return a corresponding
        HITRANPrm object.

        """

        this_prm = HITRANPrm()
        this_prm.name, this_prm.value, this_prm.error, this_prm.ref = row[5:]
        return this_prm

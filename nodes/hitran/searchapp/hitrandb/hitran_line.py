# hitran_line.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
from hitran_state import *

class HITRANLine:

    def __init__(self):
        self.nu = None; self.nu_err = None
        self.A = None; self.A_err = None
        self.Eupper = None; self.Elower = None
        self.statep = None; self.statepp = None
        self.strline = None
        self.molecID = None; self.isoID = None
        self.S = None; self.S_err = None
        self.gp = None; self.gpp = None
        self.multipole = None
        self.stateIDp = None; self.stateIDpp = None
        self.statep = None; self.statepp = None
        self.prms = {}

    @classmethod
    def parse_from_mysql(self, row):
        """
        Parse a MySQL row from the trans table of the HITRAN database
        for information about a HITRAN line and return a corresponding
        HITRANLine object.

        """

        this_line = HITRANLine()
        this_line.id, this_line.molecID, this_line.isoID,\
            this_line.InChIKey, this_line.stateIDpp, this_line.stateIDp,\
            this_line.nu, this_line.nu_err, this_line.nu_ref,\
            this_line.S, this_line.S_err, this_line.S_ref,\
            this_line.A, this_line.A_err, this_line.A_ref,\
            this_line.multipole,\
            this_line.Elower, this_line.gp, this_line.gpp,\
            this_line.datestamp, this_line.Ierr = row

        # attach states with as much information as we've gleaned from
        # parsing this transitions MySQL row to this_line:
        try:
            self.Eupper = this_line.nu + this_line.Elower
        except TypeError:
            # Elower was None, so we can't calculate Eupper
            pass

        # if we're attaching State objects, do it here:
        #this_line.statep = HITRANState(this_line.molecID, this_line.isoID,
        #    None, this_line.Eupper, this_line.gp)
        #this_line.statepp = HITRANState(this_line.molecID, this_line.isoID,
        #    None, this_line.Elower, this_line.gpp)

        # finally, return the instance of the new line created:
        return this_line

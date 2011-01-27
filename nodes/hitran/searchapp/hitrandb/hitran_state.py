# hitran_state.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
#
# Defines a class, State, to describe molecular states.

class HITRANState:

    def __init__(self, molecID, isoID, stateqn, E, g):
        self.molecID = molecID
        self.isoID = isoID
        if stateqn is None:
            self.stateqn = None
        else:
            self.stateqn = dict(stateqn)
        self.E = E
        self.g = g

    @classmethod
    def parse_from_mysql(self, row):
        """
        Parse a MySQL row from the states table of the HITRAN database
        for information about a HITRAN state and return a corresponding
        HITRANState object.

        """

        stateID, molecID, isoID, InChIKey, assigned, energy, \
            energy_err, energy_flag, g, caseID, qns = row
        this_state = HITRANState(molecID, isoID, None, energy, g)

        return this_state         

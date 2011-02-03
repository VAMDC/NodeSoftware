# hitran_request.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
# http://www.ucl.ac.uk/~ucapch0/
#
# Defines the HITRANRequest class representing a request for a particular
# of lines from the HITRAN database.

# v0.3 now uses an XML format to represent the HITRAN request.

import sys
from xml.sax import make_parser
#from HITRANRequestHandler import *
from output_txt import *
#from Output.OutputPAR import *
#from Output.OutputXML import *

class HITRANRequest:
    """
    A class representing a request for a particular set of lines from the
    HITRAN database.

    Methods:
    __init__()    Initialise an instance of the HITRANRequest class, loading
            the request data from file req_name
    read_request_file()    Read the HITRAN request file
    """

    def __init__(self, meta, req_name=None):
        """
        Initialise an instance of the HITRANRequest class.
        
        Class attributes:
        isoIDmax - the maximum isotopologue ID to search for
        numin - the minimum wavenumber (in cm-1) of the search
        numax - the maximum wavenumber (in cm-1) of the search
        Smin - the minimum HITRAN line strength (in cm-1/(molec.cm-2))
        molecules - a list of molecule names to search for
        molecIDs - the corresponding list of molecule IDs to search for

        Arguments:
        meta - a HITRANmeta object, containing meta-data about the HITRAN
            database
        req_name - the filename of the HITRAN request file

        """

        self.isoIDmax = None
        self.numin = None
        self.numax = None
        self.Smin = None
        self.molecules = []
        self.molecIDs = []

        # the compression type for output files: None, 'gz' or 'bz2'
        self.compression = None
        # the field separator character(s) to use for text-file output
        self.separator = ''
        # by default, we weight the line strengths by isotopologue abundance
        self.weight_S = True
        # do we need to fetch the states (ie quantum numbers) as well as the
        # transitions?
        self.get_states = False

        self.outputs = []
        self.param_list = []

        if req_name is not None:
            self.read_request_file(meta, req_name)

    def convert_units(self, num, from_units, to_units):
        """
        Convert the quantity num from units from_units
        to units to_units. Its value in the new units
        is returned.
        """

        if from_units == to_units:
            return num
        if from_units == 'nm':
            num = 1.e7/num
        elif from_units == 'um':
            num = 1.e4/num
        elif from_units == 'Hz':
            num /= 2.99792458e10
        elif from_units == 'kHz':
            num /= 2.99792458e7
        elif from_units == 'MHz':
            num /= 2.99792458e4
        elif from_units == 'GHz':
            num /= 29.9792458
        elif from_units == 'THz':
            num /= 2.99792458e-2
        else:
            print 'HITRANRequest: unrecognised from_units:',from_units
            sys.exit(1)

        if to_units == 'cm-1':
            return num
        else:
            print 'HITRANRequest: unrecognised to_units:',units
            sys.exit(1)

    def read_request_file(self, meta, req_name):
        """
        Parse an input file requesting a particular set of lines
        from the HITRAN database.

        """

        XML_format = False
        input = open(req_name,'r')
        for line in input:
            line = line.strip()
            if not line: continue
            if line.startswith('<?xml'):
                XML_format = True
                break
            else:
                break
        input.close()

        if XML_format:
            self.read_XML_request_file(meta, req_name)
        else:
            print '%s appears not to be an XML file' % req_name
            sys.exit(1)

        # self.molecIDs is the list of molecule IDs to search for;
        # it corresponds directly to the self.molecules list
        self.molecIDs = [meta.molec_id[molec_name] for molec_name in
                self.molecules]

    def read_XML_request_file(self, meta, req_name):
        """
        Parse an input file requesting a particular set of lines
        from the HITRAN database. The request file is in XML.

        """

        print 'reading XML HITRAN request file:',req_name
        
        parser = make_parser()
        reqHandler = HITRANRequestHandler()
        parser.setContentHandler(reqHandler)
        parser.parse(open(req_name))
        ##print reqHandler.sql_str
        for restriction in reqHandler.restriction_list:
            if restriction.param == 'nu':
                if restriction.type=='min':
                    self.numin = self.convert_units(restriction.value,
                        restriction.units,'cm-1')
                elif restriction.type == 'max':
                    self.numax = self.convert_units(restriction.value,
                        restriction.units,'cm-1')
            elif restriction.param == 'S':
                if restriction.type == 'min':
                    self.Smin = restriction.value
            elif restriction.param == 'molec_name':
                if restriction.type == 'in':
                    self.molecules = restriction.value
                if restriction.type == 'eq':
                    self.molecules = [restriction.value]
            elif restriction.param == 'isoID':
                if restriction.type == 'max':
                    self.isoIDmax = restriction.value
        # check numin and numax are the right way round:
        if self.numin > self.numax:
            self.numin, self.numax = self.numax, self.numin

        # the reqHandler class sets up Output objects as it parses the
        # XML, so copy that puppy across to this HITRANRequest object
        # where it's needed:
        self.get_states = False
        self.outputs = reqHandler.outputs
        # do we need to retrieve the states (ie quantum numbers)?
        for output in self.outputs:
            self.get_states = self.get_states or output.get_states 
 
        self.compression = reqHandler.compression
        self.separator = reqHandler.separator

    def setup_output_objects(self, output_formats, filestem, compression,
                             param_list, fixed_format, sep=''):
        for output_format in output_formats:
            if output_format == 'txt':
                self.outputs.append(OutputTXT(filestem,
                                compression, param_list, fixed_format, sep))
            elif output_format == 'xml':
                self.outputs.append(OutputXML(filestem,
                                    compression, param_list))
            elif output_format == 'par':
                self.outputs.append(OutputPAR(filestem,
                                    compression, param_list))


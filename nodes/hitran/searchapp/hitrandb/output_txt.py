# output_txt.py
# v0.2, 18/01/11
# v0.1, 22/06/10
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
#
# Defines the OutputTXT class for outputing results of a HITRAN query in
# ASCII text table formatted output.
import sys
import re
from output import *

line_attr_dict = {'E"': 'Elower', "E'": 'Eupper', 'g"': 'gpp', "g'": 'g',
                  'nu': 'nu', 'nu_err': 'nu_err', 'S': 'S', 'S_err': 'S_err',
                  'A': 'A', 'A_err': 'A_err'}

class OutputTXT(Output):
    def __init__(self, filestem, compression=None, fields=[],
                 fixed_format=False, separator=''):

        # strip the extension (which is added later) if present:
        if filestem.endswith('.txt'):
            filestem = filestem[:-4]

        Output.__init__(self, filestem, compression)
        self.fields = fields
        self.nfields = len(fields)
        self.fixed_format = fixed_format
        self.separator = separator
        self.output_header = True
        self.get_states = False

    def header(self):
        header_fields=[]
        for field in self.fields:
            header_fields.append(field)

        return header_fields

    def write_output(self, linelist, statelist):
        """
        Output the selected lines to file(s) <txt_name>-<molec_name>.txt as
        an ASCII text table with fields separated by sep and compressed with
        the algorithm described by the string compression.

        """

        if not linelist:
            print 'no lines to write!'
            return

        #if self.fixed_format:
        #    fmt = ''.join([ffmt for ffmt in self.fixed_format])
        if self.fixed_format:
            blanks = []
            patt = '%(\d+)+'
            for fmt in self.fixed_format:
                m = re.match(patt, fmt)
                if not m:
                    print 'failed to parse patt for',fmt
                    sys.exit(1)
                blanks.append(' ' * int(m.group(1)))

        filename = '%s.txt' % self.filestem
        output = open(filename, 'w')
        header_fields = self.header()
        if self.output_header and not self.fixed_format:
            print >>output, self.separator.join(header_fields)
        for line in linelist:
            s_fields = [''] * self.nfields
            vals = [''] * self.nfields
            stateIDp = line.stateIDp
            stateIDpp = line.stateIDpp
            for i, field in enumerate(self.fields):
                try:
                    val = getattr(line, line_attr_dict[field], None)
                except KeyError:
                    prm = line.prms.get(field)
                    if prm is not None:
                        val = prm.value
                    else:
                        print 'unknown field:',field
                        sys.exit(1)
                if self.fixed_format:
                    if val is not None:
                        s_fields[i] = self.fixed_format[i] % val
                    else:
                        s_fields[i] = blanks[i]
                else: 
                    if val is not None:
                        s_fields[i] = str(val)
            print >>output, self.separator.join(s_fields)
        output.close()

        tar_name = '%s-txt.tar.%s' % (self.filestem, self.compression)
        self.compress(tar_name, self.filenames)
        return filename

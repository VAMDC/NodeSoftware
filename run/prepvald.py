#!/usr/bin/env python

"""
Import tool for preparing the VALD raw data for importing.
relates the term information to the vald3 database lines into
one merged file that can be parsed directly by the import mechanisms.

Run this inside the directory containing the vald3 and term raw files
to create two new files, one for terms and one for states. 
"""

import os

def charrange(line, start, end):
    "Extract substring by indexes"
    return line[start:end]

def make_vald_upperstate_key(line, jnum=None):
    "Create an unique upper state identifier string"
    if not jnum:
        # jnum not supplied: get it from vald3 line
        jnum = charrange(line, 77, 82).strip()   
    species = charrange(line, 30, 36)
    coup = charrange(line, 170, 172)
    term = charrange(line, 172, 218)
    tstate = tuple(str(t).strip() for t in (species, coup, jnum, term))
    if not (tstate[1] and tstate[2]):
        return 'Unknown'
    return '%s-%s-%s-%s' % tstate

def make_vald_lowerstate_key(line, jnum=None):
    "Create an unique lower state identifier string"
    if not jnum:
        # jnum not supplied: get it from vald3 line
        jnum = charrange(line, 58, 63).strip()     
    species = charrange(line, 30, 36)
    coup = charrange(line, 122, 124)
    term = charrange(line, 124, 170)
    tstate = tuple(str(t).strip() for t in (species, coup, jnum, term))
    if not (tstate[1] and tstate[2]):
        return 'Unknown'
    return '%s-%s-%s-%s' % tstate

def create_state_file(valdfile_filename, output_filename):
    """
    Extracts the state information and tucks it into an intermediary
    file that don't have any duplicates.
    """

    vald_file = open(valdfile_filename)
    output_file = open(output_filename, 'w')

    # How to extract upper states 
    upperconf = [          
        {'cname':'charid',  
         'cbyte':(make_vald_upperstate_key,())},
        {'cname':'species',
        'cbyte':(charrange,(30,36))},
        {'cname':'energy',
         'cbyte':(charrange,(63,77))},
        #{'cname':'j',   
        # 'cbyte':(charrange,(77,82)),},
        {'cname':'lande',
         'cbyte':(charrange,(88,94)),
         'cnull':'99.00'},
        {'cname':'coupling',
         'cbyte':(charrange,(170,172))},
        {'cname':'term',
         'cbyte':(charrange,(172,218))},
        {'cname':'energy_ref',
         'cbyte':(charrange,(264,268))},
        {'cname':'lande_ref',
         'cbyte':(charrange,(268,272))},
        {'cname':'level_ref',
         'cbyte':(charrange,(284,288))},
        ] # end of column def list
    

    # How to extract lower states
    lowerconf = [
        {'cname':'charid',  
         'cbyte':(make_vald_lowerstate_key,())},
        {'cname':'species',
         'cbyte':(charrange,(30,36))},
        {'cname':'energy',
         'cbyte':(charrange,(44,58))},
        #{'cname':'j',
        # 'cbyte':(charrange,(58,63))},
        {'cname':'lande',
         'cbyte':(charrange,(82,88)),
         'cnull':'99.00'},
        {'cname':'coupling',
         'cbyte':(charrange,(122,124))},
        {'cname':'term',
         'cbyte':(charrange,(124,170))},
        {'cname':'energy_ref',
         'cbyte':(charrange,(260,264))},
        {'cname':'lande_ref',
         'cbyte':(charrange,(268,272))},
        {'cname':'level_ref',
         'cbyte':(charrange,(284,288))},
        ] # end of column def    

    # create state file 

    vald_file.readline()
    vald_file.readline()

    for line in vald_file:
        if line.startswith('#'):
            continue        
        for conf in [upperconf, lowerconf]:
            # process each line twice,
            # to get upper and lower states respectively
            for colconf in conf:
                func = colconf['cbyte'][0]
                args = colconf['cbyte'][1]
                data = func(line, *args)
                if data and not (colconf.has_key('cnull')
                                 and data == colconf['cnull']): 
                    output_file.write(data.strip())
                output_file.write(';')
            output_file.write('\n')


def create_transition_file(valdfile_filename, output_filename):
    """
    Creates a pre-processed file for the transitions.
    """
    vald_file = open(valdfile_filename)
    output_file = open(output_filename, 'w')

    transitionconf = [           
        {'cname':'vacwave',
         'cbyte':(charrange,(0,15))},  
        {'cname':'airwave',
         'cbyte':(charrange,(15,30))},  
        {'cname':'species',
         'cbyte':(charrange,(30,36))},
        {'cname':'loggf',
         'cbyte':(charrange,(36,44))},
        {'cname':'landeff',
         'cbyte':(charrange,(94,100)),
         'cnull':'99.00'},
        {'cname':'gammarad',
         'cbyte':(charrange,(100,107)),
         'cnull':'0.0'},
        {'cname':'gammastark',
         'cbyte':(charrange,(107,114)),
         'cnull':'0.0'},
        {'cname':'gammawaals',
         'cbyte':(charrange,(114,122)),
         'cnull':'0.0'},
        {'cname':'srctag',
         'cbyte':(charrange,(218,225))},
        {'cname':'acflag',
         'cbyte':(charrange,(225,226))},
        {'cname':'accur',
         'cbyte':(charrange,(226,236))},
        {'cname':'comment',
         'cbyte':(charrange,(236,252))},
        {'cname':'wave_ref',
         'cbyte':(charrange,(252,256))},
        {'cname':'loggf_ref',
         'cbyte':(charrange,(256,260))},
        {'cname':'lande_ref',
         'cbyte':(charrange,(268,272))},
        {'cname':'gammarad_ref',
         'cbyte':(charrange,(272,276))},
        {'cname':'gammastark_ref',
         'cbyte':(charrange,(276,280))},
        {'cname':'gammawaals_ref',
         'cbyte':(charrange,(280,284))},
        {'cname':'upstateid',
         'cbyte':(make_vald_upperstate_key,())},
        {'cname':'lostateid',
         'cbyte':(make_vald_lowerstate_key,())},
        {'cname':'upstate',
         'cbyte':(make_vald_upperstate_key,())},
        {'cname':'lostate',
         'cbyte':(make_vald_lowerstate_key,())}
        ]

    # create transition file
    
    vald_file.readline()
    vald_file.readline()
    
    for line in vald_file:
        if line.startswith('#'):
            continue
        for colconf in transitionconf:
            func = colconf['cbyte'][0]
            args = colconf['cbyte'][1]
            data = func(line, *args)
            if data and not (colconf.has_key('cnull')
                             and data == colconf['cnull']):
                output_file.write(data.strip())
            output_file.write(';')
        output_file.write('\n')

def create_term_file(valdfile_filename, termfile_filename, output_filename):
    """
    Reads the vald3 data file sequentially, relating each line to the
    corresponding line in the term file and output to a merged (unsorted, non-unique)
    file.   
    """

    # open i/o files

    vald_file = open(valdfile_filename,'r')
    term_file = open(termfile_filename,'r')
    output_file = open(output_filename,'w')

    for iline, vald_line in enumerate(vald_file):

        if iline < 2:
            term_file.readline()
            term_file.readline()
            continue

        if vald_line.startswith('#'):
            continue

        for hl in ('lo','hi'):
            # match vald3 line-numbers with the term file
            # (they match by line number)
            # we handle upper and lower states in sequence.
            
            term_line = term_file.readline().strip()

            if term_line == 'Unknown' or term_line == '':
                # ditch unsuitable lines
                continue

            # extract info from term file 
            qcoup, qnames, qvals = term_line.split(':')

            # set the variables to the correct values,
            # or to 'X' if it doesn't exist
            qdict = dict(zip(qnames.split(','),
                             [float(v) for v in qvals.split(',')]))
            J = qdict.get('J', 'X')
            L = qdict.get('L', 'X')
            S = qdict.get('S', 'X')
            parity = qdict.get('parity', 'X')
            J1 = qdict.get('J1', 'X')
            J2 = qdict.get('J2', 'X')
            K = qdict.get('K', 'X')
            S2 = qdict.get('S2', 'X')
            Jc = qdict.get('Jc', 'X')
            
            # build unique id string from info in the vald3 file + the J info.
            if hl == 'lo':
                idstring = make_vald_lowerstate_key(vald_line, J)
            else:
                idstring = make_vald_upperstate_key(vald_line, J)

            output_file.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % \
                           (idstring, J, L, S, parity, J1, J2, K, S2, Jc))
    # safety close
    vald_file.close()
    term_file.close()
    output_file.close()

def run_sortu(filename):
    """
    Run the unix command sort -u on the file. This sorts the file and
    makes each line unique (supposedly this is more efficient than to
    do it line by line in Python)
    """    
    os.popen("sort -u %s >& %s_temp && mv %s_temp %s" % \
             (filename, filename, filename, filename))
    
if __name__ == '__main__':    
    
    # i/o files
    
    vald_filename = 'vald3_500.dat'
    #vald_filename = 'vald3_atomic_obs.dat'
    term_filename =  'terms'
    #vald3_filename = '/vald/vald3_atomic_obs.dat'
    #term_filename = '/vald/terms'

    term_out_filename = 'terms_preprocessed.dat'
    transitions_out_filename = 'transitions_preprocessed.dat'
    states_out_filename = 'states_preprocessed.dat'

    # running
    print "Creating Term file by merging %s and %s ... " % (vald_filename,
                                                            term_filename)
    create_term_file(vald_filename, term_filename,
                     term_out_filename)
    print "Creating State file from %s ..." % vald_filename
    create_state_file(vald_filename, states_out_filename)
    print "Creating Transition file from %s ..." % vald_filename
    create_transition_file(vald_filename, transitions_out_filename)

    print "Running 'sort -u' on all output files ... "
    run_sortu(term_out_filename)
    run_sortu(states_out_filename)
    run_sortu(transitions_out_filename)
    print "Created files '%s', '%s' and '%s'." % \
          (term_out_filename, states_out_filename, transitions_out_filename)

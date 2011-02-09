# hitran.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
# http://www.ucl.ac.uk/~ucapch0/

import sys
import time
import MySQLdb
from hitran_line import *
from hitran_prm import *
from hitran_source import *
from output_txt import *

class HITRAN:
    """
    A class for searching the MySQL HITRAN database.

    """

    def __init__(self, req):
        self.req = req

    def read_db(self):
        """
        Do the MySQL Query

        """

        search_summary = {}

        dbname = 'HITRAN'
        username = 'christian'
        conn = MySQLdb.connect(host="localhost", user=username,
                db=dbname, read_default_file="/etc/my.cnf")
        cursor = conn.cursor()

        command = 'SELECT molecID, molec_name_html FROM molecules WHERE'\
          ' molecID in (%s)' % ','.join([str(id) for id in self.req.molecIDs])
        cursor.execute(command)

        search_summary['molec_name_html'] = [row[1]
                                for row in cursor.fetchall()]

        sourceIDs = set()
        restrictions=[]
        start = time.time()
        if self.req.molecIDs:
            s_molecid_list = []
            restrictions.append('molecID IN (%s)' % ', '.join(
                ['%d' % molecID for molecID in self.req.molecIDs]))

        if self.req.isoIDmax:
            restrictions.append('isoID<=%d' % self.req.isoIDmax)

        if self.req.numin:
            restrictions.append('nu>=%s' % str(self.req.numin))
        if self.req.numax:
            restrictions.append('nu<=%s' % str(self.req.numax))

        if self.req.Smin:
            restrictions.append('S>=%s' % str(self.req.Smin))

        s_restrictions = ' AND '.join(restrictions)
        command = 'SELECT * FROM trans WHERE %s ORDER BY nu' % s_restrictions
        print command; sys.stdout.flush()
        cursor.execute(command)
        ntrans = cursor.rowcount
        search_summary['ntrans'] = ntrans
        end = time.time()
        print '%d transitions retrieved in %.1f secs' % (ntrans,
                (end - start))

        # parse and store the lines, and get the unique stateIDs
        linelist = []
        stateIDs = set()
        start = time.time()
        for row in cursor.fetchall():
            this_line = HITRANLine.parse_from_mysql(row)
            stateIDs.add(this_line.stateIDp)
            stateIDs.add(this_line.stateIDpp)
            sourceIDs.add(this_line.nu_ref)
            sourceIDs.add(this_line.S_ref)
            sourceIDs.add(this_line.A_ref)
            self.attach_prms(this_line, cursor, this_line.id, sourceIDs)
            linelist.append(this_line)
        search_summary['nstates'] = len(stateIDs)
        end = time.time()
        print '%d transitions parsed in %.1f secs' % (ntrans,
                (end - start))

        statelist = []
        start = time.time()
        if self.req.get_states:
            for stateID in stateIDs:
                command = 'SELECT * FROM states where id="%s"' % stateID
                cursor.execute(command)
                for row in cursor.fetchall():
                    this_state = HITRANState.parse_from_mysql(row)
                    statelist.append(this_state)
        end = time.time()
        print '%d states retrieved in %.1f secs' % (len(statelist),
                (end - start))

        sourcelist = []
        for sourceID in sourceIDs:
            command = 'SELECT * FROM refs WHERE sourceID="%s"' % sourceID
            cursor.execute(command)
            row = cursor.fetchone()
            if row:
                this_source = HITRANSource.parse_from_mysql(row)
                if this_source:
                    sourcelist.append(this_source)

        search_summary['filenames'] = []
        for output in self.req.outputs:
            # NB XXX we can't do much about sources, for now
            filename = output.write_output(linelist, statelist)        
            search_summary['filenames'].append(filename)

        return search_summary

    def attach_prms(self, line, cursor, transID, sourceIDs):
        """
        Determine the parameters for this line, add them to the line's
        prm dictionary, and keep the sourceIDs list up-to-date.

        """
        command = 'SELECT * FROM prms WHERE transID="%s"' % transID
        cursor.execute(command)
        for row in cursor.fetchall():
            this_prm = HITRANPrm.parse_from_mysql(row)
            line.prms[this_prm.name] = this_prm
            sourceIDs.add(this_prm.ref)


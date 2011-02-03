# hitran_source.py
# v0.1, 18/1/11
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk

class HITRANSource:

    def __init__(self):
        """
        Initialise a Source object

        """

        self.sourceID = None
        self.type = None
        self.authors = []
        self.title = None
        self.journal = None
        self.volume = None
        self.pages = (None, None)
        self.year = None
        self.institution = None
        self.note = None
        self.doi = None

    @classmethod
    def parse_from_mysql(self, row):
        """
        Parse the array, row, which is the output of a MySQLdb
        query on the refs table into a Source object.

        """

        source = HITRANSource()

        source.sourceID = row[0]
        source.type = row[1]
        s_author = row[2]
        source.authors = s_author.split(' and ')
        source.title = row[3]
        source.journal = row[4]
        source.volume = row[5]
        if row[6] is not None:
            pages = row[6].split('--')
            start_page = pages[0]
            end_page = None
            if len(pages)>1:
                end_page = pages[1]
            source.pages = (start_page, end_page)
        source.year = row[7]
        source.institution = row[8]
        source.note = row[9]
        source.doi = row[10]

        return source

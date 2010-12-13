from DjNode.tapservice.sqlparse import SQL

class TapQuery(object):
    def __init__(self,data):
        try:
            self.request = data['REQUEST'].lower()
            self.lang = data['LANG'].lower()
            self.query=data['QUERY']
            self.format = data['FORMAT'].lower()
            self.isvalid=True
        except:
            self.isvalid=False
            raise

        if self.isvalid: self.validate()
        if self.isvalid: self.parseSQL()

    def validate(self):
        """
        overwrite this method for
        custom checks, depending on data set
        """

    def parseSQL(self):
        self.parsedSQL=SQL.parseString(self.query)

    def __str__(self):
        return '%s'%self.query



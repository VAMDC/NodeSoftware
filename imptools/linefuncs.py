"""
Line functions are helper functions available to use in the mapping file.

All importable line functions take 'linedata' as a first argument.
This can be either a string (the current active line), or a list of strings in the case of lines from many files being read simultaneously. In the latter case, the argument 'filenum' is used to select the correct line. For linefuncs accepting a single line, this selection must be made in the mapping dictionary.

Example of call from mapping dictionary:

 {'cname' : 'whatever_field_name', 
  'cbyte' : (charrange, 56, 58)}

"""
import string

# is_iter checks if a variable is iterable (a list, tuple etc) or not.
# Returns True/False.
def is_iter(iterable):
    """
    Helper function
    
    Checks if the given argument is iterable or not, i.e. if it
    is a list or tuple. Strings are not considered iterable by
    this function.
    """    
    return hasattr(iterable, '__iter__')

# Line funcs
def constant(linedata,value):
    return value

def charrange(linedata, start, end, filenum=0):
    """
    Cut out part of a line of texts based on indices.

    Inputs:
     linedata (str or iterable) - current line(s) to operate on
     start, end (int) - beginning and end indices of the line
     filenum (int) - optional selection of line if linedata is an iterable
    
    """
    if is_iter(linedata):
        linedata = linedata[filenum]        
    try:
        return linedata[start:end].strip()
    except Exception, e:
        #print "charrange skipping '%s': %s (%s)" % (linedata, e)        
        pass
    
def charrange2int(linedata, start, end, filenum=0):
    """
    Cut out part of a line based on indices, return as integer

    Inputs:
      linedata (str or iterable) - current line(s) to operate on
      start, end (int) - beginning and end indices of the line
      filenum (int) - optional selection of line if linedata is an iterable
   
    """
    if is_iter(linedata):
        linedata = linedata[filenum] 
    try:
        return int(round(float(linedata[start:end].strip())))
    except Exception, e:
        #print "ERROR: charrange2int: %s: %s" % (linedata, e)
        pass
        
def bySepNr(linedata, number, sep=','):
    try: 
        return string.split(linedata,sep)[number].strip()
    except Exception, e:
        pass
        #print "ERROR: bySepNr skipping line '%s': %s" % (linedata, e)

def bySepNr2(linedata, number, sep=',', filenum=0):
    """
    Split a text line by sep argument and return
    the number:ed split section

    Inputs:
      linedata (str or iterable) - current line(s) to operate on
      number (int) - nth section, separated by sep
      sep (str) - a separator to split by
      filenum (int) - optional selection of line if linedata is an iterable   

    """
    if is_iter(linedata):
        linedata = linedata[filenum] 
    try:
        return linedata.split(sep)[number].strip()
    except Exception, e:
        pass
        #print "ERROR: bySepNr skipping line '%s': %s" % (linedata, e)

def lineSplit(linedata, splitsep=',', filenum=0):
    """
    Splits a line by splitsep, returns a list. The main use for this
    method is creating a many-to-many reference.

    Inputs:
      linedata (str or iterable) - current line(s) to operate on
      splitsep (str) - string to split by
      filenum (int) - optional selection of line if linedata is an iterable   

    Returns a list!      
    """    

    if is_iter(linedata):
        linedata = linedata[filenum]    
    try:
        return [string.strip() for string in linedata.split(splitsep)]
    except Exception, e:
        #print "ERROR: linesplit %s: %s" % (linedata, e)
        pass



#
# VALD-specific examples below
#

def get_srcfile_ref(linedata, sep1, sep2):
    "extract srcfile reference"
    l1 = bySepNr(linedata, sep1)
    l2 = bySepNr(l1, sep2, '/')
    return l2.strip("'").strip()

def get_publications(linedata):
    "extract publication data. This returns a list since it is for a multi-reference."
    return [p.strip() for p in bySepNr(linedata, 4, '||').split(',')]

def get_term_val(linedata, varname):
    """
    extract configurations from term file. 
      varname is the value type we want (e.g. s or l); we search the identifyer field of the 
              term-file to see if it exists and return the corresponding value, otherwise
              we return 'X'. 
    """
    line=linedata[1] # we know we want the second file of the pair (the term file)!
    # the line consists of 3 parts- coupling:identifiers:values . Coupling we get already from transition file. 
    parts = line.split(':')    
    if len(parts) < 3:
        return 'X'
    # parse the identifier part of the line
    idlist = [p.strip() for p in parts[1].split(',')]
    try:
        # get the correct section of the value part of the file, if it exists
        return parts[2].split(',')[idlist.index(varname)]
    except ValueError, IndexError:
        return 'X'
  
def get_gammawaals(linedata, sep1, sep2):
    "extract gamma - van der waal value"
    l1 = charrange(linedata, sep1, sep2)    
    if float(l1) < 0:
        return l1
    else:
        return '0.000'

def get_alphawaals(linedata, sep1, sep2):
    "extract alpha - van der waal value"
    l1 = charrange(linedata, sep1, sep2)    
    if float(l1) > 0:
        return "%s.%s" % (0, bySepNr(l1, 1, '.'))
    else:
        return '0.000'    

def get_sigmawaals(linedata, sep1, sep2):
    "extract sigma - van der waal value"
    l1 = charrange(linedata, sep1, sep2)   
    if float(l1) > 0:
        return bySepNr(l1, 0, '.')
    else:
        return '0.000'

def get_accur(linedata, range1, range2):
    "extract accuracy"
    return "%s,%s" % (charrange(linedata, *range1), charrange(linedata, *range2))

def merge_cols(linedata, *ranges):
    """
    Merges data from several columns into one, separating them with '-'.
     ranges are any number of tuples (indexstart, indexend) defining the columns.
    """
    return '-'.join([charrange(linedata, *ran) for ran in ranges])
    
def merge_cols_by_sep(linedata, *sepNr):
    """
    Merges data from several columns (separated by ;) into one, separating them with '-'.
    sepNr are the nth position of the file, separated by 'sep'.
    Assumes a single line input.
    """    
    sep = ';'
    return '-'.join([bySepNr(linedata, nr, sep=sep).strip() for nr in sepNr])

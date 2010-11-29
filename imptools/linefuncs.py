"""
Line functions are helper functions available to use in the mapping file.

All importable line functions take 'linedata' as a first argument.
This can be either a string (the current active line), or a list of strings in the case of lines from many files being read simultaneously. In the latter case, the argument 'filenum' is used to select the correct line. For linefuncs accepting a single line, this selection must be made in the mapping dictionary.

Example of call from mapping dictionary:

 {'cname' : 'whatever_field_name', 
  'cbyte' : (charrange, 56, 58)}

"""

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
        
def bySepNr(linedata, number, sep=',', filenum=0):
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

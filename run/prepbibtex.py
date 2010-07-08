"""
 Test implementation for parsing bibtex reference files.

 Keeping this in a separate file from prepvald.py since
 this one is quite generically usable and has no specifi
 vald-dependencies.  

"""
import sys

def get_entries_from_file(filename):
    """
    Opens a .bib file and extracts all entries
    starting with @ (@article, @book etc)

    The available python libraries related to
    bibtex seem mostly interested in extracting .aux files
    rather than already nicely formatted bibtex files. In
    the end it was easier to just hand-code it, although
    one need to look into it again for building a
    more generic module. 
    """
    try:
        bibfile = open(filename, 'r')
    except IOError:
        print "No bibtex file found."
        sys.exit()
        
    # get all lines, stripping TeX comments
    biblines = r"\n".join([line.strip() for line in bibfile.readlines()
                          if line and not line.strip().startswith('%')])
    # split the file by @, yet retain the starting @
    bibentries = ["@%s" % line for line in biblines.split('@') if line]

    return bibentries
    
def parse_bibtex_entry(entry, dbref_key="note"):
    """
    Parses bibtech entries on the form

    @article{refname,
      author =       {{LastName}, A. and {LastName}, A, B.},
      %  title =       {},
      journal =      'Journal',
      year =         2042,
      volume =       42,
      pages =       442,
      note = '(SR)'
      }
      Returns a dict with the fields as well as the raw entry. 

      The dbref_field argument denotes which of the fields will be
      stored as the primary database ref key (dbref) of the
      entry. If the dbref argument is given
      as an empty string, the refname is used.
      If the dbref_key key/refname is not found, the entry is skipped and
      the error is reported.
    """
    field_dict = {'raw_entry':'', 'entry_type':'',
                  "bibref":'', 'errors':""}      

    # strip all unneccesary whitespaces
    entry = r" ".join(word for word in entry.split())

    # we store the full entry for easy retreaval later
    field_dict['raw_entry'] = entry

    # now that we've stored the raw entry, strip bibtex markup
    entry = " ".join(line for line in entry.split(r'\n')).strip()
    entry = entry.strip()
    entry = entry.lstrip('@')
    entry = entry.rstrip('}')
    
    # entrytype (most often 'article')
    entrytype, entry = entry.split('{', 1)     
    field_dict['entry_type'] = entrytype
    field_list = [field.strip() for field in entry.split(',')]

    # we have a list of all fields.     
    if not field_list:
        return field_dict

    # the first (?) field is the reference name #TODO: check bibtex standard

    field_dict["bibref"] = field_list.pop(0)

    # next, we loop through all the fields and add them to dict
    fieldkey = "errors"        
    fieldval = ""
    for field in field_list:
        if '=' in field:
            fieldkey, fieldval = [arg.strip() for arg in field.split('=')]
            field_dict[fieldkey] = fieldval.replace('{','').replace('}','')       
        else:
            # there was a comma, but the field is not yet over (e.g. an author name)
            # - append this to the previously found field instead of creating a new one.
            field = field.strip().replace('{','').replace('}','')   
            field_dict[fieldkey] = "%s, %s" % (field_dict[fieldkey], field)        

    # store one of the entries as a special dbref field.
    if dbref_key:
        dbref = field_dict.get(dbref_key, None)
        if not dbref:
            print "entry '%s' do not have a valid key '%s'. Ignoring this entry." % (field_dict["bibref"], dbref_key)
            return None 
    else:
        # if no dbref_key was given, use the refname
        dbref = field_dict["bibref"]

    field_dict['dbref'] = dbref
    return field_dict


def create_bibtex_preprocessed_file(bibtex_file,
                                    outfilename="publications_preprocessed.dat"):
    """
    Takes a bibtech file and converts it into a format
    suitable for reading by the database importer

    dbref || ref || author || raw bibtex entry

    
    """

    outfile = open(outfilename, 'w')

    # extract bibtex entries from file
    bibentries = get_entries_from_file(bibtex_file)

    # we create an interim file, splitting out author and the raw_bibtex into
    # the model (for now) using '||' as separator.
    string = ""
    for ib, bibentry in enumerate(bibentries):
        entry_dict = parse_bibtex_entry(bibentry)
        if not entry_dict:
            continue
        
        if entry_dict['errors'] or not 'author' or not entry_dict["bibref"] or '||' in entry_dict["raw_entry"]:
            raise Exception("There were errors in parsing entry %s (%s).\n unparsed text: %s" % 
                            (entry_dict['dbref'], entry_dict["bibref"], entry_dict['errors']))
        string += "\n%s||%s||%s||" % (entry_dict["dbref"], entry_dict["bibref"], entry_dict["author"])
        string += r"%s" % entry_dict["raw_entry"]
    # save 
    outfile.write(string)
    outfile.close()
    print "Finished parsing bibtex file. Created output file %s." % outfilename

if __name__ == "__main__":
    filename = "/home/samreg/Project/VAMDC/vamdc-git/imptools/vald_raw/refs/vald3_new_ref.bib"
    create_bibtex_preprocessed_file(filename)

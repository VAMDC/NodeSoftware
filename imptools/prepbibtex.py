#!/usr/bin/python

"""
 Test implementation for parsing bibtex reference files.

 Keeping this in a separate file from prepvald.py since
 this one is quite generically usable and has no specific
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
    one need to look into it again for building an even
    more generic module. 
    """
    try:
        bibfile = open(filename, 'r')
    except IOError:
        print "No bibtex file found."
        sys.exit()
        
    # get all lines, stripping TeX comments
    biblines = r"\n".join([line.strip() for line in bibfile.readlines()
                          if line.strip() and not line.strip().startswith('%')])
    # split the file by @, yet retain the starting @
    bibentries = ["@%s" % line for line in biblines.split('@') if line]
    return bibentries
    
def parse_bibtex_entry(entry, dbref_key="bibref"):
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
    #print entry
    
    # we store the full entry for easy retreaval later
    field_dict['bibtex'] = entry

    # now that we've stored the raw entry, strip bibtex markup
    entry = " ".join(line for line in entry.split(r'\n')).strip()
    entry = entry.strip()
    entry = entry.lstrip('@')
    entry = entry.rstrip('}')
    
    # entrytype (most often 'article')
    entrytype, entry = entry.split('{', 1)     
    field_dict['category'] = entrytype
    field_list_temp = [field for field in entry.split(',')]
    field_list = []
    lcurb = rcurb = 0
    temp = ""
    for field in field_list_temp:
        lcurb += field.count('{')
        rcurb += field.count('}')        
        temp += field
        if lcurb == rcurb:
            field_list.append(temp.strip())
            lcurb = rcurb = 0
            temp = ""
    if temp:
        field_list.append(temp.rstrip('}').strip())

    # we have a list of all fields.     
    if not field_list:
        return field_dict

    # the first (?) field is the reference name #TODO: check bibtex standard

    field_dict["bibref"] = field_list.pop(0)
    
    # next, we loop through all the fields and add them to dict. To do this we assume they
    # all are defined on a key = value format.
    print "field_list: ", field_list
    for field in field_list:
        if '=' in field:
            fieldkey, fieldval = [arg.strip() for arg in field.split('=', 1)]
            field_dict[fieldkey.lower()] = fieldval.replace('{','').replace('}','')       
        else:
            # malformed field
            field_dict["errors"] = field

    print field_dict
    # store one of the entries as a special dbref field.
    if dbref_key:
        dbref = field_dict.get(dbref_key.lower(), None)
        if not dbref:
            print "entry '%s' do not have a valid key '%s'. Ignoring this entry." % (field_dict["bibref"], dbref_key)
            return None 
    else:
        # if no dbref_key was given, use the refname
        dbref = field_dict["bibref"]

    field_dict['dbref'] = dbref
    return field_dict


def create_bibtex_preprocessed_file(bibtex_file,
                                    outfilename,
                                    field_map,
                                    dbref_key='bibref'):
    """
    Takes a bibtech file and converts it into a format
    suitable for reading by the database importer

    dbref || ref || author || etc ...

    
    """

    outfile = open(outfilename, 'w')

    # extract bibtex entries from file
    bibentries = get_entries_from_file(bibtex_file)

    # we create an interim file, splitting out author and the raw_bibtex into
    # the model (for now) using '||' as separator.
    string = ""
    for ib, bibentry in enumerate(bibentries):
        entry_dict = parse_bibtex_entry(bibentry, dbref_key=dbref_key)
        if not entry_dict:
            continue
        string += "||".join([entry_dict.get(fieldname.lower(),"") for fieldname in field_map])
        string += "\n"
        
        # if entry_dict['errors'] or not entry_dict.has_key('author') or not entry_dict["bibref"] or '||' in entry_dict["bibtex"]:
        #     raise Exception("There were errors in parsing entry %s (%s).\n unparsed text: %s" % 
        #                     (entry_dict['dbref'], entry_dict["bibref"], entry_dict['errors']))
        # string += "\n%s||%s||%s||" % (entry_dict["dbref"].strip('"').lstrip('(').rstrip(')'), entry_dict["bibref"], entry_dict["author"])
        # string += "%s" % entry_dict["bibtex"].encode("string-escape") # retain all line breaks
    string = string.strip()
    # save 
    outfile.write(string)
    outfile.close()
    print "Finished parsing bibtex file. Created output file %s." % outfilename

if __name__ == "__main__":
    #filename = "/vald/vald3_new_ref.bib"
    infile = "VALD3_ref.bib"
    outfile = "publications_preprocessed.dat"

    field_map = ["dbref", "bibref", "Author", "Title", "Category", "Year", "Journal", "Volume", "Page", "Bdsk-Url-1", "bibtex"]
    create_bibtex_preprocessed_file(infile, outfile, field_map, dbref_key="bibref")
